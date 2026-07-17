"""Execution middleware contracts.

This module defines the internal middleware object model used to build the
request execution pipeline between runtime orchestration and transport
execution.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import TypeAlias

from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.settings import RuntimeSettings


@dataclass(slots=True, frozen=True)
class ExecutionContext:
    """Describe internal state for a single request execution.

    Purpose:
        Separate immutable runtime configuration from request-scoped execution
        state without exposing per-request orchestration details as public API.

    Parameters:
        original_request: Original request submitted by the caller.
        request: Effective request being executed by the transport.
        settings: Runtime configuration applied to the request.

    Attributes:
        original_request: Original request submitted by the caller.
        request: Effective request being executed by the transport.
        settings: Runtime configuration applied to the request.

    Raises:
        No additional exceptions are raised after successful construction.

    Usage Notes:
        This object is internal only and may evolve independently of the public
        API.
    """

    original_request: HttpRequest
    request: HttpRequest
    settings: RuntimeSettings

    def with_request(self, request: HttpRequest) -> "ExecutionContext":
        """Return a new execution context with an updated effective request.

        Args:
            request: Updated request to be executed by the transport.

        Returns:
            A new execution context containing the updated request.
        """
        return replace(self, request=request)


ExecutionHandler: TypeAlias = Callable[[ExecutionContext], HttpResponse]


class ExecutionMiddleware(ABC):
    """Define the contract for internal request execution middleware.

    Purpose:
        Standardize how middleware participates in the request execution
        pipeline without coupling the runtime to individual behaviors such as
        authentication, retry, or rate limiting.

    Parameters:
        This abstract interface does not define constructor parameters.

    Attributes:
        Concrete middleware implementations own any behavior-specific state.

    Raises:
        Implementations may later raise normalized runtime exceptions.

    Usage Notes:
        Middleware is internal infrastructure. It is intentionally excluded from
        the stable public API surface.
    """

    @abstractmethod
    def handle(
        self,
        *,
        context: ExecutionContext,
        next_handler: ExecutionHandler,
    ) -> HttpResponse:
        """Process one execution step and delegate to the next handler.

        Args:
            context: Internal execution state for one request.
            next_handler: Remaining middleware pipeline or terminal executor.

        Returns:
            A future normalized HTTP response.
        """


def compose_middleware(
    *,
    middleware: tuple[ExecutionMiddleware, ...],
    terminal_handler: ExecutionHandler,
) -> ExecutionHandler:
    """Compose middleware into one execution handler.

    Args:
        middleware: Ordered middleware sequence to apply.
        terminal_handler: Final execution handler, typically transport
            invocation.

    Returns:
        One execution handler that applies middleware in declaration order.
    """
    handler = terminal_handler

    for current_middleware in reversed(middleware):
        next_handler = handler

        def handler(
            context: ExecutionContext,
            *,
            current_middleware: ExecutionMiddleware = current_middleware,
            next_handler: ExecutionHandler = next_handler,
        ) -> HttpResponse:
            return current_middleware.handle(
                context=context,
                next_handler=next_handler,
            )

    return handler
