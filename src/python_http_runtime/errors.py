"""HTTP runtime exception hierarchy.

This module defines the repository exception model used across runtime,
transport, middleware, and higher-level integration boundaries.
"""

from __future__ import annotations


class HttpRuntimeError(Exception):
    """Base exception for package-level HTTP runtime failures.

    Purpose:
        Provide a stable root exception for runtime-related failures so callers
        can catch package-level errors consistently.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This class serves as the package root exception and is not raised
        directly for normal operational categories.

    Usage Notes:
        More specific transport, timeout, response, and middleware exceptions
        derive from this base type.
    """


class HttpConfigurationError(HttpRuntimeError):
    """Describe invalid runtime or request configuration state.

    Purpose:
        Signal that runtime settings or request declarations are structurally
        invalid before any transport execution occurs.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This exception will be used when construction or orchestration detects
        invalid configuration state.

    Usage Notes:
        Configuration failures are distinct from transport and remote response
        failures.
    """


class HttpTransportError(HttpRuntimeError):
    """Describe failures produced by the transport layer.

    Purpose:
        Normalize low-level transport implementation failures into a stable
        package-specific error category.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This exception will later wrap failures produced by concrete transport
        implementations.

    Usage Notes:
        Original transport exceptions should be preserved as chained context.
    """


class HttpTimeoutError(HttpTransportError):
    """Describe request execution timeouts.

    Purpose:
        Represent timeout failures as a dedicated transport error subtype.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This exception will later be raised when request execution exceeds the
        configured timeout contract.

    Usage Notes:
        Timeouts are modeled separately from other transport failures because
        they often require different retry and reporting behavior.
    """


class HttpResponseError(HttpRuntimeError):
    """Describe HTTP response failures surfaced by runtime policy.

    Purpose:
        Reserve a category for HTTP status-based failure handling when runtime
        execution policy chooses to surface certain responses as exceptions.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This exception will later be raised by response-handling policy, not by
        the transport contract itself.

    Usage Notes:
        Transport success and application-level HTTP failure are intentionally
        modeled as different concepts.
    """


class HttpMiddlewareError(HttpRuntimeError):
    """Describe failures originating from middleware execution.

    Purpose:
        Reserve a distinct category for middleware orchestration failures that
        are not transport failures and not remote response failures.

    Parameters:
        This exception accepts the standard ``Exception`` initialization
        arguments only.

    Attributes:
        No additional public attributes are defined.

    Raises:
        This exception will later be used when middleware violates execution
        contracts or produces unrecoverable orchestration failures.

    Usage Notes:
        Middleware-specific failures should still preserve original exception
        context when normalized by the runtime.
    """

