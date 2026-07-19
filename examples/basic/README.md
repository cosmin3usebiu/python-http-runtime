# Basic Example

This example uses `MockTransport` so it remains deterministic and offline.

```python
from python_http_runtime import HttpRequest, HttpResponse, HttpRuntime
from python_http_runtime import RuntimeSettings
from python_http_runtime.testing import MockTransport

transport = MockTransport(outcomes=(HttpResponse(status_code=200, body=b"ok"),))
runtime = HttpRuntime(
    settings=RuntimeSettings(base_url="https://api.example.com"),
    transport=transport,
)

response = runtime.execute(HttpRequest(method="GET", target="/health"))
```

`MockTransport` is a documented public testing submodule API candidate. It is
not exported from the package root.

This example does not perform live HTTP and does not validate a concrete network
transport.
