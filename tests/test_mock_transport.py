"""Tests for the deterministic mock transport."""

from __future__ import annotations

import pytest

from python_http_runtime.errors import (
    HttpConfigurationError,
    HttpTimeoutError,
    HttpTransportError,
)
from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.testing import MockTransport


def test_mock_transport_returns_queued_response() -> None:
    """Verify the mock transport returns the next queued response."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(
        outcomes=(
            HttpResponse(status_code=200, body=b"ok"),
        ),
    )

    response = transport.execute(request)

    assert response.status_code == 200
    assert response.body == b"ok"
    assert response.request is request


def test_mock_transport_records_requests_in_execution_order() -> None:
    """Verify the mock transport records requests in the order executed."""
    first_request = HttpRequest(method="GET", target="/first")
    second_request = HttpRequest(method="POST", target="/second")
    transport = MockTransport(
        outcomes=(
            HttpResponse(status_code=200),
            HttpResponse(status_code=201),
        ),
    )

    transport.execute(first_request)
    transport.execute(second_request)

    assert transport.requests == (first_request, second_request)


def test_mock_transport_rebinds_response_to_executed_request() -> None:
    """Verify returned responses reference the request actually executed."""
    original_request = HttpRequest(method="GET", target="/original")
    queued_response = HttpResponse(
        status_code=202,
        request=original_request,
    )
    executed_request = HttpRequest(method="GET", target="/actual")
    transport = MockTransport(outcomes=(queued_response,))

    response = transport.execute(executed_request)

    assert response.request is executed_request
    assert response.request is not original_request


def test_mock_transport_raises_queued_transport_error() -> None:
    """Verify the mock transport surfaces queued normalized transport errors."""
    request = HttpRequest(method="GET", target="/health")
    queued_error = HttpTimeoutError("Timed out.")
    transport = MockTransport(outcomes=(queued_error,))

    with pytest.raises(HttpTimeoutError, match="Timed out."):
        transport.execute(request)


def test_mock_transport_wraps_non_normalized_exception() -> None:
    """Verify the mock transport wraps generic exceptions consistently."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport(outcomes=(ValueError("Socket failure"),))

    with pytest.raises(
        HttpTransportError,
        match="Mock transport encountered a non-normalized execution exception.",
    ) as exc_info:
        transport.execute(request)

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Socket failure"


def test_mock_transport_rejects_missing_queued_outcome() -> None:
    """Verify the mock transport rejects execution without queued outcomes."""
    request = HttpRequest(method="GET", target="/health")
    transport = MockTransport()

    with pytest.raises(
        HttpTransportError,
        match="Mock transport has no queued outcome for request execution.",
    ):
        transport.execute(request)


def test_mock_transport_rejects_invalid_outcome_configuration() -> None:
    """Verify the mock transport rejects unsupported queued outcome types."""
    with pytest.raises(
        HttpConfigurationError,
        match=(
            "Mock transport outcomes must be HttpResponse or Exception instances."
        ),
    ):
        MockTransport(outcomes=(object(),))
