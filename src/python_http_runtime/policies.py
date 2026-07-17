"""Execution policy placeholders.

This module defines internal middleware placeholders for retry and rate-limit
behavior without implementing those policies yet.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from python_http_runtime.errors import HttpConfigurationError, HttpTransportError
from python_http_runtime.middleware import (
    ExecutionContext,
    ExecutionHandler,
    ExecutionMiddleware,
)
from python_http_runtime.response import HttpResponse


@dataclass(slots=True)
class RetryMiddleware(ExecutionMiddleware):
    """Describe placeholder retry middleware.

    Purpose:
        Reserve the object model for retry behavior while keeping execution
        policy logic outside the runtime orchestrator.

    Parameters:
        max_attempts: Planned maximum number of execution attempts.

    Attributes:
        max_attempts: Placeholder retry attempt limit.

    Raises:
        No additional exceptions are raised by pass-through placeholder
        behavior.

    Usage Notes:
        Retry algorithms and retryable-error classification are deferred to a
        later milestone. This middleware is intentionally pass-through until
        retry behavior is implemented.
    """

    max_attempts: int = 1

    def __post_init__(self) -> None:
        """Validate retry middleware configuration."""
        if isinstance(self.max_attempts, bool) or not isinstance(
            self.max_attempts,
            int,
        ):
            raise HttpConfigurationError(
                "Retry middleware max_attempts must be an integer."
            )

        if self.max_attempts < 1:
            raise HttpConfigurationError(
                "Retry middleware max_attempts must be greater than or equal to one."
            )

    def handle(
        self,
        *,
        context: ExecutionContext,
        next_handler: ExecutionHandler,
    ) -> HttpResponse:
        """Apply retry policy behavior.

        Args:
            context: Internal execution state for one request.
            next_handler: Remaining middleware pipeline.

        Returns:
            The downstream response produced by the remaining pipeline.
        """
        for attempt_index in range(self.max_attempts):
            try:
                return next_handler(context)
            except HttpTransportError:
                if attempt_index == self.max_attempts - 1:
                    raise

        raise AssertionError("Retry middleware exhausted without returning or raising.")


@dataclass(slots=True)
class RateLimitMiddleware(ExecutionMiddleware):
    """Describe placeholder rate-limit middleware.

    Purpose:
        Reserve the object model for rate-limit enforcement while keeping
        throttling logic outside the runtime orchestrator.

    Parameters:
        rate_limit_key: Placeholder identifier for a future rate-limit bucket.

    Attributes:
        rate_limit_key: Placeholder rate-limit bucket identifier.

    Raises:
        No additional exceptions are raised by pass-through placeholder
        behavior.

    Usage Notes:
        Waiting strategy and quota tracking are deferred to a later milestone.
        This middleware is intentionally pass-through until rate-limit behavior
        is implemented.
    """

    rate_limit_key: str = "default"
    minimum_interval_seconds: float = 0.0
    _time_provider: Callable[[], float] = field(default=time.monotonic, repr=False)
    _sleep: Callable[[float], None] = field(default=time.sleep, repr=False)
    _last_execution_started_at: float | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate rate-limit middleware configuration."""
        if not isinstance(self.rate_limit_key, str) or not self.rate_limit_key.strip():
            raise HttpConfigurationError(
                "Rate-limit middleware requires a non-empty rate_limit_key."
            )

        if (
            isinstance(self.minimum_interval_seconds, bool)
            or not isinstance(self.minimum_interval_seconds, (int, float))
        ):
            raise HttpConfigurationError(
                "Rate-limit middleware minimum_interval_seconds must be an "
                "int or float."
            )

        if self.minimum_interval_seconds < 0:
            raise HttpConfigurationError(
                "Rate-limit middleware minimum_interval_seconds must be "
                "greater than or equal to zero."
            )

    def handle(
        self,
        *,
        context: ExecutionContext,
        next_handler: ExecutionHandler,
    ) -> HttpResponse:
        """Apply rate-limit policy behavior.

        Args:
            context: Internal execution state for one request.
            next_handler: Remaining middleware pipeline.

        Returns:
            The downstream response produced by the remaining pipeline.
        """
        current_time = self._time_provider()

        if self._last_execution_started_at is not None:
            elapsed_seconds = current_time - self._last_execution_started_at
            remaining_seconds = self.minimum_interval_seconds - elapsed_seconds
            if remaining_seconds > 0:
                self._sleep(remaining_seconds)
                current_time = self._time_provider()

        self._last_execution_started_at = current_time
        return next_handler(context)
