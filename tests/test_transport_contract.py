"""Tests for the transport contract."""

from __future__ import annotations

import pytest

from python_http_runtime.request import HttpRequest
from python_http_runtime.response import HttpResponse
from python_http_runtime.transport import Transport


def test_transport_contract_is_abstract() -> None:
    """Verify the transport contract cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Transport()


class StaticTransport(Transport):
    """Provide a minimal concrete transport for contract verification."""

    def execute(self, request: HttpRequest) -> HttpResponse:
        """Return a fixed response for the provided request."""
        return HttpResponse(
            status_code=200,
            body=b"ok",
            request=request,
        )


def test_concrete_transport_implements_minimal_contract() -> None:
    """Verify a concrete transport accepts a request and returns a response."""
    request = HttpRequest(method="GET", target="/health")
    transport = StaticTransport()

    response = transport.execute(request)

    assert response.status_code == 200
    assert response.body == b"ok"
    assert response.request is request
