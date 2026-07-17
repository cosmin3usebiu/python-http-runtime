"""Tests for immutable HTTP response boundary objects."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from python_http_runtime.errors import HttpConfigurationError
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse


def test_response_normalizes_headers_body_and_elapsed_time() -> None:
    """Verify response construction normalizes stable boundary metadata."""
    request = HttpRequest(method="GET", target="/health")
    response = HttpResponse(
        status_code=200,
        headers={
            " Content-Type ": " application/json ",
            "X-Trace-Id": " abc-123 ",
        },
        body=bytearray(b'{"ok": true}'),
        elapsed_seconds=0,
        request=request,
    )

    assert response.status_code == 200
    assert response.headers == {
        "content-type": "application/json",
        "x-trace-id": "abc-123",
    }
    assert response.body == b'{"ok": true}'
    assert response.elapsed_seconds == 0.0
    assert response.request is request


def test_response_freezes_header_mapping() -> None:
    """Verify response header mappings are immutable after construction."""
    response = HttpResponse(
        status_code=204,
        headers={"X-Test": "value"},
    )

    assert isinstance(response.headers, MappingProxyType)

    with pytest.raises(TypeError):
        response.headers["x-test"] = "other"


@pytest.mark.parametrize("status_code", [99, 600, True, "200"])
def test_response_rejects_invalid_status_code(status_code: object) -> None:
    """Verify response construction rejects invalid status codes."""
    with pytest.raises(HttpConfigurationError):
        HttpResponse(
            status_code=status_code,  # type: ignore[arg-type]
        )


def test_response_rejects_invalid_header_value_type() -> None:
    """Verify response construction rejects non-string header values."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP header values must be strings.",
    ):
        HttpResponse(
            status_code=200,
            headers={"X-Test": 1},
        )


def test_response_rejects_invalid_body_type() -> None:
    """Verify response construction rejects unsupported body representations."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP response body must be bytes, bytearray, or memoryview.",
    ):
        HttpResponse(
            status_code=200,
            body="payload",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("elapsed_seconds", [-0.1, True, "1.5"])
def test_response_rejects_invalid_elapsed_time(elapsed_seconds: object) -> None:
    """Verify response construction rejects invalid elapsed duration values."""
    with pytest.raises(HttpConfigurationError):
        HttpResponse(
            status_code=200,
            elapsed_seconds=elapsed_seconds,  # type: ignore[arg-type]
        )


def test_response_rejects_invalid_request_metadata() -> None:
    """Verify response construction rejects invalid originating request objects."""
    with pytest.raises(
        HttpConfigurationError,
        match="HTTP response request metadata must be an HttpRequest or None.",
    ):
        HttpResponse(
            status_code=200,
            request="invalid",  # type: ignore[arg-type]
        )


def test_response_accepts_memoryview_body() -> None:
    """Verify response construction normalizes memoryview bodies into bytes."""
    response = HttpResponse(
        status_code=200,
        body=memoryview(b"abc"),
    )

    assert response.body == b"abc"
