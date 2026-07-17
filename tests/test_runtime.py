"""Tests for runtime orchestration behavior."""

from __future__ import annotations

from dataclasses import dataclass

from python_http_runtime.auth import ApiKeyHeaderMiddleware, BearerTokenMiddleware
from python_http_runtime.middleware import (
    ExecutionContext,
    ExecutionHandler,
    ExecutionMiddleware,
)
from python_http_runtime.policies import RateLimitMiddleware, RetryMiddleware
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.runtime import HttpRuntime
from python_http_runtime.settings import RuntimeSettings
from python_http_runtime.testing import MockTransport


def test_runtime_executes_request_through_transport() -> None:
    """Verify the runtime delegates effective request execution to transport."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200, body=b"ok"),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
    )

    response = runtime.execute(request)

    assert response.status_code == 200
    assert response.body == b"ok"
    assert response.request is not None
    assert response.request.method == "GET"
    assert response.request.target == "https://api.example.com/health"


def test_runtime_merges_default_headers_and_request_headers() -> None:
    """Verify request headers override runtime defaults during execution."""
    request = HttpRequest(
        method="GET",
        target="/health",
        headers={
            "x-trace-id": "request-trace",
        },
    )
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(
            base_url="https://api.example.com",
            default_headers={
                "x-client-id": "runtime-client",
                "x-trace-id": "runtime-trace",
            },
        ),
        transport=transport,
    )

    runtime.execute(request)

    executed_request = transport.requests[0]
    assert executed_request.headers == {
        "x-client-id": "runtime-client",
        "x-trace-id": "request-trace",
    }


def test_runtime_prefers_request_timeout_override() -> None:
    """Verify request-local timeout overrides runtime default timeout."""
    request = HttpRequest(
        method="GET",
        target="/health",
        timeout_seconds=5,
    )
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(
            base_url="https://api.example.com",
            default_timeout_seconds=30,
        ),
        transport=transport,
    )

    runtime.execute(request)

    assert transport.requests[0].timeout_seconds == 5.0


def test_runtime_uses_default_timeout_when_request_override_missing() -> None:
    """Verify runtime default timeout is applied when request omits one."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(
            base_url="https://api.example.com",
            default_timeout_seconds=30,
        ),
        transport=transport,
    )

    runtime.execute(request)

    assert transport.requests[0].timeout_seconds == 30.0


def test_runtime_preserves_absolute_targets() -> None:
    """Verify absolute request targets are not rewritten by the runtime."""
    request = HttpRequest(
        method="GET",
        target="https://other.example.com/status",
    )
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
    )

    runtime.execute(request)

    assert transport.requests[0].target == "https://other.example.com/status"


def test_runtime_executes_middleware_in_declared_order() -> None:
    """Verify runtime applies middleware in declaration order."""
    call_log: list[str] = []

    @dataclass(slots=True)
    class RecordingMiddleware(ExecutionMiddleware):
        name: str

        def handle(
            self,
            *,
            context: ExecutionContext,
            next_handler: ExecutionHandler,
        ) -> HttpResponse:
            call_log.append(f"{self.name}:before")
            response = next_handler(context)
            call_log.append(f"{self.name}:after")
            return response

    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(
            RecordingMiddleware(name="first"),
            RecordingMiddleware(name="second"),
        ),
    )

    runtime.execute(request)

    assert call_log == [
        "first:before",
        "second:before",
        "second:after",
        "first:after",
    ]


def test_runtime_passes_execution_context_through_placeholder_middleware() -> None:
    """Verify pass-through placeholder middleware does not alter orchestration."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(
            BearerTokenMiddleware(token="secret"),
            ApiKeyHeaderMiddleware(header_name="x-api-key", api_key="secret"),
            RetryMiddleware(max_attempts=3),
            RateLimitMiddleware(rate_limit_key="default"),
        ),
    )

    response = runtime.execute(request)

    assert response.status_code == 200
    assert transport.requests[0].target == "https://api.example.com/health"


def test_runtime_response_references_effective_executed_request() -> None:
    """Verify the returned response references the executed effective request."""
    original_request = HttpRequest(
        method="GET",
        target="/health",
        headers={"x-request-id": "abc-123"},
    )
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(
            base_url="https://api.example.com",
            default_headers={"x-client-id": "runtime"},
        ),
        transport=transport,
    )

    response = runtime.execute(original_request)

    assert response.request is not None
    assert response.request is not original_request
    assert response.request.target == "https://api.example.com/health"
    assert response.request.headers == {
        "x-client-id": "runtime",
        "x-request-id": "abc-123",
    }
