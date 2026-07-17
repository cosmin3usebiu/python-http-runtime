"""HTTP request model definitions.

This module defines the immutable public request object model used by the
runtime. Request execution behavior is intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, TypeAlias

from python_http_runtime.errors import HttpConfigurationError

HeaderMapping: TypeAlias = Mapping[str, str]
QueryValue: TypeAlias = str | int | float | bool
QueryParameterMapping: TypeAlias = Mapping[str, QueryValue]


@dataclass(slots=True, frozen=True, kw_only=True)
class HttpRequest:
    """Describe one HTTP request to be executed by the runtime.

    Purpose:
        Provide an immutable, transport-agnostic request model that callers can
        pass into the runtime without embedding transport implementation
        details.

    Parameters:
        method: HTTP method such as ``GET`` or ``POST``.
        target: Absolute URL or relative target path to be executed.
        headers: Optional request header mapping.
        query_params: Optional query parameter mapping.
        body: Optional raw request body.
        timeout_seconds: Optional per-request timeout override.

    Attributes:
        method: HTTP method to execute.
        target: Absolute URL or relative target path.
        headers: Optional request header mapping.
        query_params: Optional query parameter mapping.
        body: Optional raw request body.
        timeout_seconds: Optional per-request timeout override.

    Raises:
        HttpConfigurationError: If request metadata is structurally invalid.

    Usage Notes:
        This object is a transport-neutral boundary value. It owns data only
        and does not contain execution or serialization behavior.
    """

    method: str
    target: str
    headers: HeaderMapping = field(default_factory=dict)
    query_params: QueryParameterMapping = field(default_factory=dict)
    body: bytes | None = None
    timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        """Normalize and validate request metadata."""
        normalized_method = self.method.strip().upper()
        normalized_target = self.target.strip()

        if not normalized_method:
            raise HttpConfigurationError("HTTP request method must be non-empty.")

        if any(character.isspace() for character in normalized_method):
            raise HttpConfigurationError(
                "HTTP request method must not contain whitespace."
            )

        if not normalized_target:
            raise HttpConfigurationError("HTTP request target must be non-empty.")

        if any(character.isspace() for character in normalized_target):
            raise HttpConfigurationError(
                "HTTP request target must not contain whitespace."
            )

        object.__setattr__(self, "method", normalized_method)
        object.__setattr__(self, "target", normalized_target)
        object.__setattr__(self, "headers", _normalize_headers(self.headers))
        object.__setattr__(
            self,
            "query_params",
            _normalize_query_params(self.query_params),
        )
        object.__setattr__(self, "body", _normalize_body(self.body))
        object.__setattr__(
            self,
            "timeout_seconds",
            _normalize_timeout_seconds(self.timeout_seconds),
        )


def _normalize_headers(headers: HeaderMapping) -> HeaderMapping:
    """Normalize request headers into an immutable lowercase mapping."""
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


def _normalize_query_params(
    query_params: QueryParameterMapping,
) -> QueryParameterMapping:
    """Normalize query parameters into an immutable mapping."""
    normalized_query_params: dict[str, QueryValue] = {}

    for parameter_name, parameter_value in query_params.items():
        if not isinstance(parameter_name, str):
            raise HttpConfigurationError("Query parameter names must be strings.")

        normalized_parameter_name = parameter_name.strip()
        if not normalized_parameter_name:
            raise HttpConfigurationError("Query parameter names must be non-empty.")

        if not isinstance(parameter_value, (str, int, float, bool)):
            raise HttpConfigurationError(
                "Query parameter values must be str, int, float, or bool."
            )

        normalized_query_params[normalized_parameter_name] = parameter_value

    return MappingProxyType(normalized_query_params)


def _normalize_body(body: bytes | None) -> bytes | None:
    """Normalize supported body representations into immutable bytes."""
    if body is None:
        return None

    if isinstance(body, bytes):
        return body

    if isinstance(body, bytearray):
        return bytes(body)

    if isinstance(body, memoryview):
        return body.tobytes()

    raise HttpConfigurationError(
        "HTTP request body must be bytes, bytearray, memoryview, or None."
    )


def _normalize_timeout_seconds(timeout_seconds: float | None) -> float | None:
    """Normalize and validate an optional timeout value."""
    if timeout_seconds is None:
        return None

    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
        raise HttpConfigurationError(
            "HTTP request timeout must be an int, float, or None."
        )

    normalized_timeout = float(timeout_seconds)
    if normalized_timeout <= 0:
        raise HttpConfigurationError("HTTP request timeout must be greater than zero.")

    return normalized_timeout
