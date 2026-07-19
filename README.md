# python-http-runtime

`python-http-runtime` is a transport-neutral HTTP execution runtime for
API-driven Python applications.

The package defines immutable request/response boundary objects, runtime
settings, a small runtime orchestrator, and a minimal transport contract. The
runtime coordinates request execution through middleware and a caller-supplied
transport implementation. It does not ship a concrete live HTTP transport.

## Governance Status

R002 is currently:

- unapproved
- unfrozen
- API not frozen
- not in Release Phase

Validation evidence, tests, and documentation updates do not approve the
repository, freeze the API, assign Release Phase, validate builds, validate
package publication, or validate live HTTP behavior.

## Package-Root Public API

The package root exports only the core runtime concepts:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

These are stable public API candidates for documentation and later freeze
review. They are not frozen public APIs yet.

## Documented Submodule APIs

R002 also contains documented submodule APIs that are not package-root exports:

- `python_http_runtime.errors`
- `python_http_runtime.auth`
- `python_http_runtime.policies`
- `python_http_runtime.testing`

The error classes, concrete authentication middleware, retry/rate-limit
middleware, and `MockTransport` are documented public submodule API candidates
for later freeze review.

## Non-Frozen Extension Contracts

The middleware extension surface is public but explicitly non-frozen/deferred:

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

These objects exist because middleware and authentication behavior use them, but
their final public extension contract is not frozen.

## Internal Implementation Details

The following objects are implementation details and should not be used as
public APIs:

- `compose_middleware`
- `MockTransportOutcome`
- `_bind_request_to_response`
- private helper functions in source modules

## What R002 Does

- Represents HTTP requests with immutable `HttpRequest` objects.
- Represents transport-neutral HTTP responses with immutable `HttpResponse`
  objects.
- Stores runtime defaults in immutable `RuntimeSettings`.
- Executes requests through `HttpRuntime`.
- Delegates request execution to a caller-supplied `Transport`.
- Supports generic header-based authentication middleware.
- Supports retry and rate-limit middleware.
- Provides `MockTransport` for deterministic tests.
- Normalizes repository errors through HTTP-specific exception classes.

## What R002 Does Not Do

R002 intentionally does not provide:

- live `requests`, `httpx`, `aiohttp`, or urllib transports
- exchange-specific signing
- exchange adapters
- market-data endpoints
- dataset persistence
- trading, strategy, or portfolio logic
- response decoding helpers such as `json()` or `text()`
- production-readiness, security-certification, or publication guarantees

Concrete live transports require a separate approved design or work package.

## Minimal Usage Shape

Applications provide a `Transport` implementation and execute immutable
requests through `HttpRuntime`.

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

This example uses an in-memory transport. It does not perform live HTTP.

## Repository Layout

- `src/python_http_runtime/` - package source
- `tests/` - behavioral tests
- `docs/` - documentation
- `examples/` - example documentation
- `.github/workflows/` - CI workflow

## Related Repositories

Depends on:

- None

Used by:

- `python-exchange-integration-runtime`
- `python-market-data-downloader`
- `python-exchange-metadata-service`
