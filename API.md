# R002 API: python-http-runtime

## Status

This document records the current R002 API boundary disposition for
documentation purposes.

R002 remains:

- unapproved
- unfrozen
- API not frozen
- not in Release Phase

The classifications below are documentation and later freeze-review candidates.
They do not approve R002, freeze the API, assign Release Phase, or declare
release readiness.

## Package-Root Public API

The package root exports exactly five objects:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

These are stable public API candidates for documentation and later freeze
review.

## Core Objects

### `HttpRequest`

Immutable request boundary object. It stores HTTP method, target, headers, query
parameters, optional body bytes, and optional per-request timeout.

### `HttpResponse`

Immutable response boundary object. It stores status code, headers, body bytes,
optional elapsed time, and optional request metadata.

`HttpResponse` intentionally does not provide response decoding helpers such as
`json()`, `text()`, `ok`, or status-category helpers.

### `RuntimeSettings`

Immutable runtime configuration object. It stores optional `base_url`, default
headers, and optional default timeout.

### `Transport`

Primary execution extension point. A transport has one responsibility:

```text
execute(HttpRequest) -> HttpResponse
```

Transport lifecycle hooks and concrete network client implementations are out
of scope for R002 unless separately approved.

### `HttpRuntime`

Runtime orchestrator. It applies settings, creates an execution context, runs
the middleware pipeline, delegates execution to `Transport`, and returns an
`HttpResponse`.

The runtime owns orchestration only. Middleware owns policy behavior. Transport
owns execution.

## Error Submodule API Candidates

The following classes are documented public submodule API candidates under
`python_http_runtime.errors`:

- `HttpRuntimeError`
- `HttpConfigurationError`
- `HttpTransportError`
- `HttpTimeoutError`
- `HttpResponseError`
- `HttpMiddlewareError`

`HttpResponseError` is reserved for response-policy failures. The current
runtime does not implement status-based response policy behavior that raises
`HttpResponseError`.

These errors are not package-root exports.

## Authentication Middleware Submodule API Candidates

The following concrete middleware classes are documented public submodule API
candidates under `python_http_runtime.auth`:

- `BearerTokenMiddleware`
- `BasicAuthMiddleware`
- `ApiKeyHeaderMiddleware`
- `CustomHeaderInjectionMiddleware`

They implement generic header-based authentication or header injection. They do
not implement exchange-specific request signing.

`AuthenticationMiddleware` is public but explicitly non-frozen/deferred as a
base/support type.

Authentication middleware is not exported from the package root.

## Policy Middleware Submodule API Candidates

The following middleware classes are documented public submodule API candidates
under `python_http_runtime.policies`:

- `RetryMiddleware`
- `RateLimitMiddleware`

Retry and rate limiting are policy middleware responsibilities. They are not
runtime responsibilities.

Policy middleware is not exported from the package root.

## Middleware Extension Contracts

The middleware extension surface is public but explicitly non-frozen/deferred:

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

These objects are visible because middleware behavior depends on them. Their
final public extension contract is deferred until a future approved API freeze
review.

The following object is internal-only:

- `compose_middleware`

## Testing Support

`MockTransport` is a documented public testing submodule API candidate under
`python_http_runtime.testing`.

It provides deterministic transport behavior for tests and examples without
performing live HTTP.

The following testing objects are internal-only implementation details:

- `MockTransportOutcome`
- `_bind_request_to_response`

`MockTransport` is not exported from the package root.

## Live HTTP Transport Non-Goal

R002 does not ship a concrete live HTTP transport.

The following implementations are out of scope unless separately approved:

- `requests` transport
- `httpx` transport
- `aiohttp` transport
- urllib transport

Users may supply their own `Transport` implementation, but R002 does not claim
live HTTP validation or production readiness.

## Unsupported Behavior

R002 does not provide:

- response decoding helpers
- exchange signing
- exchange adapters
- market-data models
- persistence
- trading/order behavior
- package publication guarantees
- build artifact validation guarantees
