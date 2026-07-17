"""Tests for immutable runtime settings."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.settings import RuntimeSettings


def test_settings_normalize_base_url_headers_and_timeout() -> None:
    """Verify runtime settings normalize stable configuration metadata."""
    settings = RuntimeSettings(
        base_url=" https://api.example.com/v1 ",
        default_headers={
            " Content-Type ": " application/json ",
            "X-Client-Id": " demo ",
        },
        default_timeout_seconds=30,
    )

    assert settings.base_url == "https://api.example.com/v1"
    assert settings.default_headers == {
        "content-type": "application/json",
        "x-client-id": "demo",
    }
    assert settings.default_timeout_seconds == 30.0


def test_settings_freeze_default_headers() -> None:
    """Verify runtime default headers are immutable after construction."""
    settings = RuntimeSettings(default_headers={"X-Test": "value"})

    assert isinstance(settings.default_headers, MappingProxyType)

    with pytest.raises(TypeError):
        settings.default_headers["x-test"] = "other"


@pytest.mark.parametrize("base_url", ["   ", "https://api example.com", 1])
def test_settings_reject_invalid_base_url(base_url: object) -> None:
    """Verify runtime settings reject invalid base URL values."""
    with pytest.raises(HttpConfigurationError):
        RuntimeSettings(base_url=base_url)  # type: ignore[arg-type]


def test_settings_reject_invalid_default_header_value_type() -> None:
    """Verify runtime settings reject non-string default header values."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP header values must be strings.",
    ):
        RuntimeSettings(default_headers={"X-Test": 1})  # type: ignore[arg-type]


@pytest.mark.parametrize("timeout_seconds", [0, -1, True, "30"])
def test_settings_reject_invalid_default_timeout(timeout_seconds: object) -> None:
    """Verify runtime settings reject invalid default timeout values."""
    with pytest.raises(HttpConfigurationError):
        RuntimeSettings(
            default_timeout_seconds=timeout_seconds,  # type: ignore[arg-type]
        )
