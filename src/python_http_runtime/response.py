"""HTTP response model definitions.

This module defines the immutable transport-neutral response object model for
the runtime. Response decoding behavior is intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.request import HeaderMapping

if TYPE_CHECKING:
    from python_http_runtime.request import HttpRequest


@dataclass(slots=True, frozen=True, kw_only=True)
class HttpResponse:
    """Describe one raw HTTP response returned by the runtime.

    Purpose:
        Provide an immutable, transport-neutral response model that exposes raw
        response information without embedding decoding helpers or client
        convenience behavior.

    Parameters:
        status_code: HTTP response status code.
        headers: Response header mapping.
        body: Raw response body bytes.
        elapsed_seconds: Optional execution duration.
        request: Optional originating request metadata.

    Attributes:
        status_code: HTTP response status code.
        headers: Response header mapping.
        body: Raw response body bytes.
        elapsed_seconds: Optional execution duration.
        request: Optional originating request metadata.

    Raises:
        HttpConfigurationError: If response metadata is structurally invalid.

    Usage Notes:
        Response decoding, text conversion, and JSON parsing are intentionally
        excluded from this repository's public model.
    """

    status_code: int
    headers: HeaderMapping = field(default_factory=dict)
    body: bytes = b""
    elapsed_seconds: float | None = None
    request: HttpRequest | None = None

    def __post_init__(self) -> None:
        """Normalize and validate response metadata."""
        from python_http_runtime.request import HttpRequest

        if isinstance(self.status_code, bool) or not isinstance(self.status_code, int):
            raise HttpConfigurationError("HTTP response status code must be an integer.")

        if self.status_code < 100 or self.status_code > 599:
            raise HttpConfigurationError(
                "HTTP response status code must be between 100 and 599."
            )

        if self.request is not None and not isinstance(self.request, HttpRequest):
            raise HttpConfigurationError(
                "HTTP response request metadata must be an HttpRequest or None."
            )

        object.__setattr__(self, "headers", _normalize_headers(self.headers))
        object.__setattr__(self, "body", _normalize_body(self.body))
        object.__setattr__(
            self,
            "elapsed_seconds",
            _normalize_elapsed_seconds(self.elapsed_seconds),
        )


def _normalize_headers(headers: HeaderMapping) -> HeaderMapping:
    """Normalize response headers into an immutable lowercase mapping."""
    normalized_headers: dict[str, str] = {}

    for header_name, header_value in headers.items():
        if not isinstance(header_name, str):
            raise HttpConfigurationError("HTTP header names must be strings.")

        if not isinstance(header_value, str):
            raise HttpConfigurationError("HTTP header values must be strings.")

        normalized_header_name = header_name.strip().lower()
        normalized_header_value = header_value.strip()

        if not normalized_header_name:
            raise HttpConfigurationError("HTTP header names must be non-empty.")

        normalized_headers[normalized_header_name] = normalized_header_value

    return MappingProxyType(normalized_headers)


def _normalize_body(body: bytes) -> bytes:
    """Normalize supported body representations into immutable bytes."""
    if isinstance(body, bytes):
        return body

    if isinstance(body, bytearray):
        return bytes(body)

    if isinstance(body, memoryview):
        return body.tobytes()

    raise HttpConfigurationError(
        "HTTP response body must be bytes, bytearray, or memoryview."
    )


def _normalize_elapsed_seconds(elapsed_seconds: float | None) -> float | None:
    """Normalize and validate an optional elapsed-duration value."""
    if elapsed_seconds is None:
        return None

    if isinstance(elapsed_seconds, bool) or not isinstance(elapsed_seconds, (int, float)):
        raise HttpConfigurationError(
            "HTTP response elapsed time must be an int, float, or None."
        )

    normalized_elapsed = float(elapsed_seconds)
    if normalized_elapsed < 0:
        raise HttpConfigurationError(
            "HTTP response elapsed time must be greater than or equal to zero."
        )

    return normalized_elapsed
