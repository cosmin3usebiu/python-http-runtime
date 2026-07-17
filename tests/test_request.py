"""Tests for immutable HTTP request boundary objects."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.request import HttpRequest


def test_request_normalizes_method_target_headers_and_timeout() -> None:
    """Verify request construction normalizes stable boundary metadata."""
    request = HttpRequest(
        method="  get  ",
        target="https://api.example.com/v1/resource",
        headers={
            " Content-Type ": " application/json ",
            "X-Request-Id": " abc-123 ",
        },
        query_params={
            " page ": 2,
            "enabled": True,
        },
        body=bytearray(b"payload"),
        timeout_seconds=30,
    )

    assert request.method == "GET"
    assert request.target == "https://api.example.com/v1/resource"
    assert request.headers == {
        "content-type": "application/json",
        "x-request-id": "abc-123",
    }
    assert request.query_params == {
        "page": 2,
        "enabled": True,
    }
    assert request.body == b"payload"
    assert request.timeout_seconds == 30.0


def test_request_freezes_header_and_query_mappings() -> None:
    """Verify request mapping attributes are immutable after construction."""
    request = HttpRequest(
        method="POST",
        target="/submit",
        headers={"X-Test": "value"},
        query_params={"page": 1},
    )

    assert isinstance(request.headers, MappingProxyType)
    assert isinstance(request.query_params, MappingProxyType)

    with pytest.raises(TypeError):
        request.headers["x-test"] = "other"

    with pytest.raises(TypeError):
        request.query_params["page"] = 2


@pytest.mark.parametrize(
    ("field_name", "field_value", "message"),
    [
        ("method", "   ", "HTTP request method must be non-empty."),
        ("method", "GET POST", "HTTP request method must not contain whitespace."),
        ("target", "   ", "HTTP request target must be non-empty."),
        (
            "target",
            "/path with spaces",
            "HTTP request target must not contain whitespace.",
        ),
    ],
)
def test_request_rejects_invalid_method_and_target(
    field_name: str,
    field_value: str,
    message: str,
) -> None:
    """Verify request construction rejects invalid method and target values."""
    request_kwargs = {
        "method": "GET",
        "target": "/health",
    }
    request_kwargs[field_name] = field_value

    with pytest.raises(HttpConfigurationError, match=message):
        HttpRequest(**request_kwargs)


def test_request_rejects_invalid_header_name() -> None:
    """Verify request construction rejects empty normalized header names."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP header names must be non-empty.",
    ):
        HttpRequest(
            method="GET",
            target="/health",
            headers={"   ": "value"},
        )


def test_request_rejects_invalid_header_value_type() -> None:
    """Verify request construction rejects non-string header values."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP header values must be strings.",
    ):
        HttpRequest(
            method="GET",
            target="/health",
            headers={"X-Test": 1},
        )


def test_request_rejects_invalid_query_parameter_name() -> None:
    """Verify request construction rejects empty normalized query names."""
    with pytest.raises(
        HttpConfigurationError,
        match="Query parameter names must be non-empty.",
    ):
        HttpRequest(
            method="GET",
            target="/health",
            query_params={"   ": 1},
        )


def test_request_rejects_invalid_query_parameter_value_type() -> None:
    """Verify request construction rejects unsupported query value types."""
    with pytest.raises(
        HttpConfigurationError,
        match="Query parameter values must be str, int, float, or bool.",
    ):
        HttpRequest(
            method="GET",
            target="/health",
            query_params={"filters": ["active"]},
        )


def test_request_rejects_invalid_body_type() -> None:
    """Verify request construction rejects unsupported body representations."""
    with pytest.raises(
        HttpConfigurationError,
        match=(
            "HTTP request body must be bytes, bytearray, memoryview, or None."
        ),
    ):
        HttpRequest(
            method="POST",
            target="/submit",
            body="payload",
        )


@pytest.mark.parametrize(
    "timeout_seconds",
    [0, -1, True, "30"],
)
def test_request_rejects_invalid_timeout(timeout_seconds: object) -> None:
    """Verify request construction rejects invalid timeout values."""
    with pytest.raises(HttpConfigurationError):
        HttpRequest(
            method="GET",
            target="/health",
            timeout_seconds=timeout_seconds,  # type: ignore[arg-type]
        )


def test_request_accepts_memoryview_body() -> None:
    """Verify request construction normalizes memoryview bodies into bytes."""
    request = HttpRequest(
        method="PUT",
        target="/binary",
        body=memoryview(b"abc"),
    )

    assert request.body == b"abc"
