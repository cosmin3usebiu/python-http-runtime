"""Tests for runtime and transport error normalization."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from python_http_runtime.errors import HttpMiddlewareError
from python_http_runtime.errors import HttpTransportError
from python_http_runtime.middleware import ExecutionContext
from python_http_runtime.middleware import ExecutionHandler
from python_http_runtime.middleware import ExecutionMiddleware
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.runtime import HttpRuntime
from python_http_runtime.settings import RuntimeSettings
from python_http_runtime.transport import Transport


def test_runtime_wraps_unknown_middleware_exceptions() -> None:
    """Verify runtime normalizes unknown middleware exceptions."""

    @dataclass(slots=True)
    class ExplodingMiddleware(ExecutionMiddleware):
        def handle(
            self,
            *,
            context: ExecutionContext,
            next_handler: ExecutionHandler,
        ) -> HttpResponse:
            del context, next_handler
            raise ValueError("Middleware boom.")

    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=StaticTransport(),
        middleware=(ExplodingMiddleware(),),
    )

    with pytest.raises(
        HttpMiddlewareError,
        match="Middleware pipeline execution failed.",
    ) as exc_info:
        runtime.execute(HttpRequest(method="GET", target="/health"))

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Middleware boom."


def test_runtime_rejects_invalid_middleware_return_values() -> None:
    """Verify runtime rejects middleware that does not return a response."""

    @dataclass(slots=True)
    class InvalidReturnMiddleware(ExecutionMiddleware):
        def handle(
            self,
            *,
            context: ExecutionContext,
            next_handler: ExecutionHandler,
        ) -> HttpResponse:
            del context, next_handler
            return "invalid"  # type: ignore[return-value]

    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=StaticTransport(),
        middleware=(InvalidReturnMiddleware(),),
    )

    with pytest.raises(
        HttpMiddlewareError,
        match="Middleware pipeline must return an HttpResponse instance.",
    ):
        runtime.execute(HttpRequest(method="GET", target="/health"))


def test_runtime_propagates_normalized_transport_errors() -> None:
    """Verify runtime propagates normalized transport failures unchanged."""

    class ExplodingTransport(Transport):
        def execute(self, request: HttpRequest) -> HttpResponse:
            del request
            raise HttpTransportError("Transport failed.")

    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=ExplodingTransport(),
    )

    with pytest.raises(HttpTransportError, match="Transport failed."):
        runtime.execute(HttpRequest(method="GET", target="/health"))


def test_runtime_wraps_unknown_transport_exceptions() -> None:
    """Verify runtime normalizes unknown transport exceptions."""

    class ExplodingTransport(Transport):
        def execute(self, request: HttpRequest) -> HttpResponse:
            del request
            raise ValueError("Socket failed.")

    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=ExplodingTransport(),
    )

    with pytest.raises(
        HttpTransportError,
        match="Transport execution failed.",
    ) as exc_info:
        runtime.execute(HttpRequest(method="GET", target="/health"))

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Socket failed."


def test_runtime_rejects_invalid_transport_return_values() -> None:
    """Verify runtime rejects transports that do not return responses."""

    class InvalidReturnTransport(Transport):
        def execute(self, request: HttpRequest) -> HttpResponse:
            del request
            return "invalid"  # type: ignore[return-value]

    runtime = HttpRuntime(
        settings=RuntimeSettings(base_url="https://api.example.com"),
        transport=InvalidReturnTransport(),
    )

    with pytest.raises(
        HttpTransportError,
        match="Transport must return an HttpResponse instance.",
    ):
        runtime.execute(HttpRequest(method="GET", target="/health"))


class StaticTransport(Transport):
    """Provide a simple valid transport for error tests."""

    def execute(self, request: HttpRequest) -> HttpResponse:
        """Return a fixed success response."""
        return HttpResponse(status_code=200, request=request)
