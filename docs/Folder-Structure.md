# Folder Structure

```text
python-http-runtime/
    src/python_http_runtime/
        __init__.py
        auth.py
        errors.py
        middleware.py
        policies.py
        request.py
        response.py
        runtime.py
        settings.py
        testing.py
        transport.py
        py.typed
    tests/
    docs/
    examples/
    .github/workflows/
```

## Source Modules

- `request.py` defines `HttpRequest`.
- `response.py` defines `HttpResponse`.
- `settings.py` defines `RuntimeSettings`.
- `transport.py` defines `Transport`.
- `runtime.py` defines `HttpRuntime`.
- `middleware.py` defines middleware support contracts and composition.
- `auth.py` defines generic auth/header middleware.
- `policies.py` defines retry and rate-limit middleware.
- `testing.py` defines `MockTransport`.
- `errors.py` defines repository-native error classes.

## Boundary Rule

Only the package-root exports are root public API. Some submodule objects are
documented public API candidates, and some implementation helpers remain
internal-only.
