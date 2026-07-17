"""Runtime orchestration object definitions.

This module defines the public runtime orchestrator interface used to execute
requests through internal middleware and a transport implementation.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from urllib.parse import urljoin

from python_http_runtime.errors import HttpMiddlewareError
from python_http_runtime.errors import HttpRuntimeError
from python_http_runtime.errors import HttpTransportError
from python_http_runtime.middleware import ExecutionContext
from python_http_runtime.middleware import ExecutionHandler
from python_http_runtime.middleware import ExecutionMiddleware
from python_http_runtime.middleware import compose_middleware
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.settings import RuntimeSettings
from python_http_runtime.transport import Transport


@dataclass(slots=True)
class HttpRuntime:
    """Coordinate HTTP request execution.

    Purpose:
        Reserve the public runtime object that will later orchestrate request
        execution across execution context construction, middleware pipeline
        execution, and transport delegation.

    Parameters:
        settings: Immutable runtime configuration object.
        transport: Transport implementation responsible for request execution.
        middleware: Ordered internal middleware pipeline.

    Attributes:
        settings: Immutable runtime configuration object.
        transport: Transport implementation responsible for request execution.
        middleware: Ordered internal middleware pipeline.

    Raises:
        No additional exceptions are raised during successful construction.

    Usage Notes:
        The runtime is an orchestrator only. Middleware owns behavior and the
        transport owns request execution.
    """

    settings: RuntimeSettings
    transport: Transport
    middleware: Sequence[ExecutionMiddleware] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Freeze middleware configuration for deterministic execution."""
        self.middleware = tuple(self.middleware)

    def execute(self, request: HttpRequest) -> HttpResponse:
        """Execute a request through the runtime.

        Args:
            request: Request to be executed.

        Returns:
            A transport-neutral response object returned by the transport.
        """
        context = ExecutionContext(
            original_request=request,
            request=_build_effective_request(
                request=request,
                settings=self.settings,
            ),
            settings=self.settings,
        )
        handler = compose_middleware(
            middleware=tuple(self.middleware),
            terminal_handler=self._execute_transport,
        )
        try:
            response = handler(context)
        except HttpRuntimeError:
            raise
        except Exception as exc:
            raise HttpMiddlewareError(
                "Middleware pipeline execution failed."
            ) from exc

        if not isinstance(response, HttpResponse):
            raise HttpMiddlewareError(
                "Middleware pipeline must return an HttpResponse instance."
            )

        return response

    def _execute_transport(self, context: ExecutionContext) -> HttpResponse:
        """Delegate effective request execution to the transport."""
        try:
            response = self.transport.execute(context.request)
        except HttpTransportError:
            raise
        except Exception as exc:
            raise HttpTransportError("Transport execution failed.") from exc

        if not isinstance(response, HttpResponse):
            raise HttpTransportError(
                "Transport must return an HttpResponse instance."
            )

        return response


def _build_effective_request(
    *,
    request: HttpRequest,
    settings: RuntimeSettings,
) -> HttpRequest:
    """Build the effective request to execute through the transport."""
    return HttpRequest(
        method=request.method,
        target=_resolve_target(request=request, settings=settings),
        headers=_merge_headers(request=request, settings=settings),
        query_params=request.query_params,
        body=request.body,
        timeout_seconds=_resolve_timeout(request=request, settings=settings),
    )


def _resolve_target(
    *,
    request: HttpRequest,
    settings: RuntimeSettings,
) -> str:
    """Resolve the transport target for one request execution."""
    if _is_absolute_target(request.target):
        return request.target

    if settings.base_url is None:
        return request.target

    base_url = settings.base_url
    if not base_url.endswith("/"):
        base_url = f"{base_url}/"

    return urljoin(base_url, request.target.lstrip("/"))


def _is_absolute_target(target: str) -> bool:
    """Return whether a request target is an absolute HTTP URL."""
    lowercase_target = target.lower()
    return lowercase_target.startswith("http://") or lowercase_target.startswith(
        "https://"
    )


def _merge_headers(
    *,
    request: HttpRequest,
    settings: RuntimeSettings,
) -> dict[str, str]:
    """Merge runtime default headers with request-specific headers."""
    merged_headers = dict(settings.default_headers)
    merged_headers.update(request.headers)
    return merged_headers


def _resolve_timeout(
    *,
    request: HttpRequest,
    settings: RuntimeSettings,
) -> float | None:
    """Resolve the effective timeout for one request execution."""
    if request.timeout_seconds is not None:
        return request.timeout_seconds

    return settings.default_timeout_seconds
