"""Package-root public interface for python-http-runtime.

The package exposes the core transport-neutral HTTP runtime objects:
HttpRuntime, HttpRequest, HttpResponse, RuntimeSettings, and Transport.
Concrete live HTTP transports are not provided by this package.
"""

from python_http_runtime import request, response, runtime, settings, transport

HttpRequest = request.HttpRequest
HttpResponse = response.HttpResponse
HttpRuntime = runtime.HttpRuntime
RuntimeSettings = settings.RuntimeSettings
Transport = transport.Transport

__all__ = [
    "HttpRequest",
    "HttpResponse",
    "HttpRuntime",
    "RuntimeSettings",
    "Transport",
]

