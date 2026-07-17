"""Tests for retry and rate-limit middleware behavior."""

from __future__ import annotations

import pytest

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.errors import HttpTimeoutError
from python_http_runtime.errors import HttpTransportError
from python_http_runtime.policies import RateLimitMiddleware
from python_http_runtime.policies import RetryMiddleware
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.runtime import HttpRuntime
from python_http_runtime.settings import RuntimeSettings
from python_http_runtime.testing import MockTransport


def test_retry_middleware_retries_transport_failures_until_success() -> None:
    """Verify retry middleware retries transport failures up to success."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(
        outcomes=(
            HttpTimeoutError("First timeout."),
            HttpResponse(status_code=200, body=b"ok"),
        ),
    )
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(RetryMiddleware(max_attempts=2),),
    )

    response = runtime.execute(request)

    assert response.status_code == 200
    assert transport.requests == (transport.requests[0], transport.requests[1])
    assert len(transport.requests) == 2


def test_retry_middleware_raises_last_transport_failure_when_exhausted() -> None:
    """Verify retry middleware raises the final transport error when exhausted."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(
        outcomes=(
            HttpTimeoutError("First timeout."),
            HttpTimeoutError("Second timeout."),
        ),
    )
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(RetryMiddleware(max_attempts=2),),
    )

    with pytest.raises(HttpTimeoutError, match="Second timeout."):
        runtime.execute(request)

    assert len(transport.requests) == 2


def test_retry_middleware_does_not_retry_non_transport_failures() -> None:
    """Verify retry middleware does not retry non-transport middleware failures."""

    class ExplodingMiddleware:
        def handle(
            self,
            *,
            context: object,
            next_handler: object,
        ) -> HttpResponse:
            del context, next_handler
            raise HttpConfigurationError("Invalid middleware state.")

    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(RetryMiddleware(max_attempts=3), ExplodingMiddleware()),
    )

    with pytest.raises(HttpConfigurationError, match="Invalid middleware state."):
        runtime.execute(HttpRequest(method="GET", target="/health"))

    assert len(transport.requests) == 0


def test_retry_middleware_rejects_invalid_configuration() -> None:
    """Verify retry middleware rejects invalid max-attempt settings."""
    with pytest.raises(
        HttpConfigurationError,
        match=(
            "Retry middleware max_attempts must be greater than or equal to one."
        ),
    ):
        RetryMiddleware(max_attempts=0)


def test_rate_limit_middleware_waits_before_subsequent_execution() -> None:
    """Verify rate-limit middleware waits to enforce a minimum interval."""
    timeline = {"now": 0.0}
    sleep_calls: list[float] = []

    def fake_time() -> float:
        return timeline["now"]

    def fake_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)
        timeline["now"] += seconds

    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(
        outcomes=(
            HttpResponse(status_code=200),
            HttpResponse(status_code=200),
        ),
    )
    middleware = RateLimitMiddleware(
        rate_limit_key="candles",
        minimum_interval_seconds=2.0,
        _time_provider=fake_time,
        _sleep=fake_sleep,
    )
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(middleware,),
    )

    runtime.execute(request)
    timeline["now"] = 1.0
    runtime.execute(request)

    assert sleep_calls == [1.0]


def test_rate_limit_middleware_rejects_invalid_configuration() -> None:
    """Verify rate-limit middleware rejects invalid configuration values."""
    with pytest.raises(
        HttpConfigurationError,
        match="Rate-limit middleware requires a non-empty rate_limit_key.",
    ):
        RateLimitMiddleware(rate_limit_key=" ")

    with pytest.raises(
        HttpConfigurationError,
        match=(
            "Rate-limit middleware minimum_interval_seconds must be greater than or equal to zero."
        ),
    ):
        RateLimitMiddleware(minimum_interval_seconds=-1.0)
