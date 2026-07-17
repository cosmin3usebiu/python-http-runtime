"""Transport abstraction definitions.

This module defines the minimal transport contract used by the runtime.
Transport lifecycle hooks and policy behavior are intentionally excluded.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse


class Transport(ABC):
    """Define the contract for HTTP transport execution.

    Purpose:
        Standardize how request execution is delegated by the runtime while
        keeping transport implementation details outside the runtime itself.

    Parameters:
        This abstract interface does not define constructor parameters.

    Attributes:
        Concrete implementations own transport-specific state and resources.

    Raises:
        Concrete implementations may later raise transport-related exceptions.

    Usage Notes:
        The transport contract intentionally exposes one responsibility only:
        execute a request and return a raw response object.
    """

    @abstractmethod
    def execute(self, request: HttpRequest) -> HttpResponse:
        """Execute one HTTP request and return a raw response.

        Args:
            request: Request to execute.

        Returns:
            A transport-neutral response object.

        Raises:
            HttpTransportError: If the transport cannot execute the request.
        """
