"""Tests for authentication middleware behavior."""

from __future__ import annotations

import base64

import pytest

from python_http_runtime.auth import ApiKeyHeaderMiddleware
from python_http_runtime.auth import BasicAuthMiddleware
from python_http_runtime.auth import BearerTokenMiddleware
from python_http_runtime.auth import CustomHeaderInjectionMiddleware
from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.runtime import HttpRuntime
from python_http_runtime.settings import RuntimeSettings
from python_http_runtime.testing import MockTransport


def test_bearer_token_middleware_injects_authorization_header() -> None:
    """Verify bearer token middleware injects an authorization header."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(BearerTokenMiddleware(token="secret-token"),),
    )

    runtime.execute(request)

    assert transport.requests[0].headers["authorization"] == "Bearer secret-token"


def test_basic_auth_middleware_injects_basic_authorization_header() -> None:
    """Verify basic auth middleware injects a base64-encoded authorization header."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(BasicAuthMiddleware(username="demo", password="secret"),),
    )

    runtime.execute(request)

    expected_value = base64.b64encode(b"demo:secret").decode("ascii")
    assert transport.requests[0].headers["authorization"] == f"Basic {expected_value}"


def test_api_key_middleware_injects_custom_header() -> None:
    """Verify API key middleware injects its configured header."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(
            ApiKeyHeaderMiddleware(header_name="X-API-Key", api_key="demo-key"),
        ),
    )

    runtime.execute(request)

    assert transport.requests[0].headers["x-api-key"] == "demo-key"


def test_custom_header_middleware_injects_multiple_headers() -> None:
    """Verify custom header middleware merges configured headers into requests."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(
            CustomHeaderInjectionMiddleware(
                headers={
                    "X-Trace-Id": "trace-123",
                    "X-Client-Name": "demo",
                }
            ),
        ),
    )

    runtime.execute(request)

    assert transport.requests[0].headers == {
        "x-trace-id": "trace-123",
        "x-client-name": "demo",
    }


def test_later_auth_middleware_overrides_earlier_header_value() -> None:
    """Verify later middleware can replace a previously injected header."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(HttpResponse(status_code=200),))
    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=transport,
        middleware=(
            CustomHeaderInjectionMiddleware(headers={"Authorization": "Bearer old"}),
            BearerTokenMiddleware(token="new-token"),
        ),
    )

    runtime.execute(request)

    assert transport.requests[0].headers["authorization"] == "Bearer new-token"


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: BearerTokenMiddleware(token=""),
            "Bearer token middleware requires a non-empty token string.",
        ),
        (
            lambda: BasicAuthMiddleware(username="", password="secret"),
            "Basic auth middleware requires a non-empty username string.",
        ),
        (
            lambda: ApiKeyHeaderMiddleware(header_name=" ", api_key="secret"),
            "API key middleware requires a non-empty header name string.",
        ),
        (
            lambda: ApiKeyHeaderMiddleware(header_name="X-API-Key", api_key=""),
            "API key middleware requires a non-empty API key string.",
        ),
        (
            lambda: CustomHeaderInjectionMiddleware(headers={}),
            "Custom header middleware requires at least one header.",
        ),
    ],
)
def test_auth_middleware_rejects_invalid_configuration(
    factory: object,
    message: str,
) -> None:
    """Verify auth middleware rejects invalid configuration."""
    with pytest.raises(HttpConfigurationError, match=message):
        factory()  # type: ignore[operator]
