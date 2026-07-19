# R002 Design: python-http-runtime

## Status

This document describes the observed R002 architecture for documentation
alignment. It does not approve R002, freeze the architecture, freeze the API,
assign Release Phase, validate builds, or declare release readiness.

R002 remains unapproved, unfrozen, API not frozen, and not in Release Phase.

## Purpose

R002 provides a reusable, transport-neutral HTTP runtime for API-driven Python
applications.

It owns generic HTTP request execution orchestration. It does not own concrete
network transports, exchange behavior, market-data models, persistence, or
trading logic.

## Core Architecture

```text
HttpRequest
    |
    v
HttpRuntime
    |
    v
ExecutionContext
    |
    v
Middleware pipeline
    |
    v
Transport
    |
    v
HttpResponse
```

The runtime coordinates the pipeline. Middleware owns policy behavior. Transport
owns request execution. Boundary objects carry data.

## Layer Responsibilities

### Request Layer

`HttpRequest` is the immutable request boundary object. It normalizes structural
request data such as method, target, headers, query parameters, body, and
per-request timeout.

### Response Layer

`HttpResponse` is the immutable response boundary object. It contains raw
transport-neutral response data only. Decoding helpers are intentionally
excluded.

### Settings Layer

`RuntimeSettings` stores immutable runtime defaults such as `base_url`, default
headers, and default timeout.

### Transport Layer

`Transport` is the primary execution extension point. It exposes only
`execute(request)`.

R002 does not ship concrete live network transports.

### Runtime Layer

`HttpRuntime` orchestrates request execution by applying settings, creating
execution state, running middleware, invoking the transport, and returning the
response.

The runtime must not contain policy algorithms, concrete transport behavior, or
domain-specific logic.

### Middleware Layer

Middleware applies behavior between runtime orchestration and transport
execution.

The middleware extension contracts are public but explicitly non-frozen/deferred:

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

`compose_middleware` is internal-only.

### Authentication Layer

R002 includes generic authentication/header-injection middleware:

- `BearerTokenMiddleware`
- `BasicAuthMiddleware`
- `ApiKeyHeaderMiddleware`
- `CustomHeaderInjectionMiddleware`

These are documented public submodule API candidates. They do not implement
exchange-specific signing.

### Policy Layer

R002 includes policy middleware:

- `RetryMiddleware`
- `RateLimitMiddleware`

These policies execute as middleware. They are not built into the runtime
orchestrator.

### Testing Layer

`MockTransport` provides deterministic in-memory transport behavior for tests
and examples. It is a documented public testing submodule API candidate.

`MockTransportOutcome` and `_bind_request_to_response` are internal-only.

### Error Layer

Repository-native errors normalize runtime, configuration, transport, timeout,
response-policy, and middleware failure categories.

`HttpResponseError` is present as a response-policy category, but current runtime
behavior does not implement status-based response policy handling that raises
it.

## Public / Private Boundary

Package-root public API:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

Documented public submodule API candidates:

- error classes
- concrete auth middleware
- retry/rate-limit middleware
- `MockTransport`

Public but non-frozen/deferred support contracts:

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

Internal-only implementation details:

- `compose_middleware`
- `MockTransportOutcome`
- `_bind_request_to_response`
- private helper functions

## Non-Goals

R002 does not own:

- live `requests`, `httpx`, `aiohttp`, or urllib transports
- exchange-specific signing
- exchange adapters
- market-data endpoints
- dataset persistence
- response decoding helpers
- trading, strategy, portfolio, or order logic
- security certification
- production-readiness or publication-readiness claims

## Dependency Policy

R002 has no runtime package dependencies.

Downstream repositories may depend on R002 public contracts, but downstream
requirements must not silently redefine R002 scope.
