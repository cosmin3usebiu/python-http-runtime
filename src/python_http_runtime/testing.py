"""Testing utility contracts.

This module defines placeholder testing utilities that will support deterministic
runtime tests without requiring live network dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence, TypeAlias

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.errors import HttpTransportError
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.transport import Transport

MockTransportOutcome: TypeAlias = HttpResponse | Exception


@dataclass(slots=True)
class MockTransport(Transport):
    """Provide a deterministic transport implementation for tests.

    Purpose:
        Execute requests against a preconfigured sequence of transport outcomes
        so runtime and middleware tests can run deterministically without live
        network dependencies.

    Parameters:
        outcomes: Ordered response or exception outcomes to replay.

    Attributes:
        outcomes: Immutable ordered sequence of queued transport outcomes.

    Raises:
        HttpConfigurationError: If the configured outcome sequence is invalid.
        HttpTransportError: If execution is attempted without a queued outcome,
            or if a queued non-normalized exception must be wrapped.

    Usage Notes:
        Mock-first testing is a core architectural principle of this repository.
        Returned responses are rebound to the executed request so recorded
        request metadata always matches actual transport input.
    """

    outcomes: Sequence[MockTransportOutcome] = field(default_factory=tuple)
    _executed_requests: list[HttpRequest] = field(default_factory=list, init=False, repr=False)
    _next_outcome_index: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        """Freeze and validate configured transport outcomes."""
        normalized_outcomes = tuple(self.outcomes)
        for outcome in normalized_outcomes:
            if not isinstance(outcome, (HttpResponse, Exception)):
                raise HttpConfigurationError(
                    "Mock transport outcomes must be HttpResponse or Exception instances."
                )

        self.outcomes = normalized_outcomes

    @property
    def requests(self) -> tuple[HttpRequest, ...]:
        """Return requests executed by the mock transport in order."""
        return tuple(self._executed_requests)

    def execute(self, request: HttpRequest) -> HttpResponse:
        """Execute a request through the mock transport.

        Args:
            request: Request to execute.

        Returns:
            A queued transport-neutral response bound to the executed request.

        Raises:
            HttpTransportError: If the next queued outcome is a transport
                failure, if no outcome remains, or if a non-normalized
                exception must be wrapped.
        """
        self._executed_requests.append(request)

        if self._next_outcome_index >= len(self.outcomes):
            raise HttpTransportError(
                "Mock transport has no queued outcome for request execution."
            )

        outcome = self.outcomes[self._next_outcome_index]
        self._next_outcome_index += 1

        if isinstance(outcome, HttpResponse):
            return _bind_request_to_response(response=outcome, request=request)

        if isinstance(outcome, HttpTransportError):
            raise outcome

        raise HttpTransportError(
            "Mock transport encountered a non-normalized execution exception."
        ) from outcome


def _bind_request_to_response(
    *,
    response: HttpResponse,
    request: HttpRequest,
) -> HttpResponse:
    """Return a response bound to the request that was actually executed."""
    return HttpResponse(
        status_code=response.status_code,
        headers=response.headers,
        body=response.body,
        elapsed_seconds=response.elapsed_seconds,
        request=request,
    )
