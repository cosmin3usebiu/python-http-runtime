"""Runtime settings object definitions.

This module defines the immutable runtime configuration model used by the HTTP
runtime. Per-request execution state is intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.request import HeaderMapping


@dataclass(slots=True, frozen=True, kw_only=True)
class RuntimeSettings:
    """Describe immutable HTTP runtime configuration.

    Purpose:
        Provide stable runtime configuration for request execution without
        mixing reusable configuration with per-request execution state.

    Parameters:
        base_url: Optional base URL used for relative request targets.
        default_headers: Optional default header mapping.
        default_timeout_seconds: Optional default timeout value.

    Attributes:
        base_url: Optional base URL used for relative request targets.
        default_headers: Optional default header mapping.
        default_timeout_seconds: Optional default timeout value.

    Raises:
        HttpConfigurationError: If runtime settings are structurally invalid.

    Usage Notes:
        Execution context is internal to the runtime and is intentionally not
        represented by this public configuration object.
    """

    base_url: str | None = None
    default_headers: HeaderMapping = field(default_factory=dict)
    default_timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        """Normalize and validate runtime configuration."""
        object.__setattr__(self, "base_url", _normalize_base_url(self.base_url))
        object.__setattr__(
            self,
            "default_headers",
            _normalize_headers(self.default_headers),
        )
        object.__setattr__(
            self,
            "default_timeout_seconds",
            _normalize_timeout_seconds(self.default_timeout_seconds),
        )


def _normalize_base_url(base_url: str | None) -> str | None:
    """Normalize and validate an optional base URL."""
    if base_url is None:
        return None

    if not isinstance(base_url, str):
        raise HttpConfigurationError("Runtime base URL must be a string or None.")

    normalized_base_url = base_url.strip()
    if not normalized_base_url:
        raise HttpConfigurationError("Runtime base URL must be non-empty when set.")

    if any(character.isspace() for character in normalized_base_url):
        raise HttpConfigurationError("Runtime base URL must not contain whitespace.")

    return normalized_base_url


def _normalize_headers(headers: HeaderMapping) -> HeaderMapping:
    """Normalize runtime default headers into an immutable lowercase mapping."""
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


def _normalize_timeout_seconds(timeout_seconds: float | None) -> float | None:
    """Normalize and validate an optional default timeout value."""
    if timeout_seconds is None:
        return None

    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
        raise HttpConfigurationError(
            "Runtime default timeout must be an int, float, or None."
        )

    normalized_timeout = float(timeout_seconds)
    if normalized_timeout <= 0:
        raise HttpConfigurationError(
            "Runtime default timeout must be greater than zero."
        )

    return normalized_timeout
