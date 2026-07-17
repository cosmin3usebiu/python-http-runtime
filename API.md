# R002 API: python-http-runtime

## Status

This is a recovered draft proposal based on observed implementation evidence.
It does not approve or freeze R002.

R002 approval/freeze state remains unverified. The API is not frozen. Release Phase is not assigned.

Current `__all__` is observed implementation evidence, not a frozen public
contract.

Any future API freeze requires explicit review and approval.

## Observed Public Exports

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

## Proposed Classification: Core Public API

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

## Proposed Classification: Public But Requires Review

- `MockTransport`
- `HttpRuntimeError`
- `HttpConfigurationError`
- `HttpTransportError`
- `HttpTimeoutError`
- `HttpResponseError`
- `HttpMiddlewareError`

## Proposed Classification: Internal Implementation Candidates

- `ExecutionContext`
- `ExecutionMiddleware`
- `compose_middleware`
- `AuthenticationMiddleware`
- `BearerTokenMiddleware`
- `BasicAuthMiddleware`
- `ApiKeyHeaderMiddleware`
- `CustomHeaderInjectionMiddleware`
- `RetryMiddleware`
- `RateLimitMiddleware`

## Known API Caveats

No concrete live HTTP transport is exported.

Middleware, auth, retry, rate limiting, mock transport, and errors are observed
implementation components but are not package-root exports.

## API Freeze Status

The API is not frozen.

This file does not approve R002, freeze R002, assign Release Phase, approve any
milestone, or declare release readiness.
