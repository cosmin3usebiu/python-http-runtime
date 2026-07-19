# Usage Examples

## Runtime With MockTransport

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

`MockTransport` is deterministic testing support and does not perform live HTTP.

## Runtime With Middleware

```python
from python_http_runtime.auth import BearerTokenMiddleware
from python_http_runtime.policies import RetryMiddleware

middleware = (
    BearerTokenMiddleware(token="example-token"),
    RetryMiddleware(max_attempts=2),
)
```

Concrete auth and policy middleware are documented public submodule API
candidates. Middleware extension contracts remain public but non-frozen/deferred.
