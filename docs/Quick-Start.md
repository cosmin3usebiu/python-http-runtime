# Quick Start

R002 requires a caller-supplied `Transport`.

```python
from python_http_runtime import HttpRequest, HttpResponse, HttpRuntime
from python_http_runtime import RuntimeSettings, Transport


class StaticTransport(Transport):
    def execute(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(status_code=200, body=b"ok", request=request)


runtime = HttpRuntime(
    settings=RuntimeSettings(base_url="https://api.example.com"),
    transport=StaticTransport(),
)

response = runtime.execute(HttpRequest(method="GET", target="/health"))
```

This example is offline and deterministic. It does not perform live HTTP.

For tests, `python_http_runtime.testing.MockTransport` can be used as a
documented public testing submodule API candidate.
