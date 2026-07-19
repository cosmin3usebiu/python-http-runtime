# API Reference

R002 exposes a small package-root API and several documented submodule API
candidates.

## Package Root

Stable public API candidates:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

These are not frozen APIs yet.

## Submodule API Candidates

Errors:

- `HttpRuntimeError`
- `HttpConfigurationError`
- `HttpTransportError`
- `HttpTimeoutError`
- `HttpResponseError`
- `HttpMiddlewareError`

Authentication middleware:

- `BearerTokenMiddleware`
- `BasicAuthMiddleware`
- `ApiKeyHeaderMiddleware`
- `CustomHeaderInjectionMiddleware`

Policy middleware:

- `RetryMiddleware`
- `RateLimitMiddleware`

Testing support:

- `MockTransport`

## Non-Frozen / Deferred Support Contracts

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

These support middleware extension behavior, but their final public contract is
not frozen.

## Internal-Only Details

- `compose_middleware`
- `MockTransportOutcome`
- `_bind_request_to_response`
- private helper functions

## Live Transport Support

R002 does not ship concrete live HTTP transports. `requests`, `httpx`,
`aiohttp`, and urllib transports are out of scope unless separately approved.
