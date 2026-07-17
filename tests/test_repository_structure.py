"""Basic repository smoke tests for the package skeleton."""

from importlib import import_module


def test_package_can_be_imported() -> None:
    """Verify that the package namespace is available."""
    module = import_module("python_http_runtime")
    assert module is not None


def test_public_exports_are_available() -> None:
    """Verify that the stable public object model is exported."""
    module = import_module("python_http_runtime")

    assert hasattr(module, "HttpRequest")
    assert hasattr(module, "HttpResponse")
    assert hasattr(module, "HttpRuntime")
    assert hasattr(module, "RuntimeSettings")
    assert hasattr(module, "Transport")


def test_public_exports_remain_minimal() -> None:
    """Verify that only the approved public API is exported."""
    module = import_module("python_http_runtime")

    assert module.__all__ == [
        "HttpRequest",
        "HttpResponse",
        "HttpRuntime",
        "RuntimeSettings",
        "Transport",
    ]


def test_internal_modules_can_be_imported() -> None:
    """Verify that the expected package modules exist."""
    module_names = (
        "python_http_runtime.auth",
        "python_http_runtime.errors",
        "python_http_runtime.middleware",
        "python_http_runtime.policies",
        "python_http_runtime.request",
        "python_http_runtime.response",
        "python_http_runtime.runtime",
        "python_http_runtime.settings",
        "python_http_runtime.testing",
        "python_http_runtime.transport",
    )

    for module_name in module_names:
        assert import_module(module_name) is not None
