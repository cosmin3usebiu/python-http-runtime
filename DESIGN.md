# R002 Design: python-http-runtime

## Status

This is a recovered draft proposal based on observed implementation evidence.
It does not approve or freeze R002.

R002 approval/freeze state remains unverified. The API is not frozen. Release Phase is not assigned.

This design is not yet approved.

## Purpose

Provide a transport-neutral HTTP execution runtime for API-driven Python
applications. The runtime coordinates request execution through immutable
request and response objects, runtime settings, middleware, and a transport
contract.

## Scope

R002 owns:

- HTTP request boundary object.
- HTTP response boundary object.
- Runtime settings.
- Runtime orchestration.
- Transport abstraction.
- Middleware composition.
- Generic authentication middleware.
- Retry middleware.
- Rate-limit middleware.
- Mock transport testing support.
- Repository-native HTTP exceptions.

## Non-Goals

R002 does not own:

- Exchange-specific signing.
- Exchange adapters.
- Market-data endpoints.
- Dataset persistence.
- Trading logic.
- Strategy logic.
- Real network transport implementations unless separately approved.
- Response decoding helpers such as JSON/text convenience APIs.
- Domain-specific HTTP semantics.

## Architecture Boundaries

Boundary models:

- `request.py`
- `response.py`
- `settings.py`

Execution layer:

- `runtime.py`
- `middleware.py`

Transport layer:

- `transport.py`
- `testing.py`

Internal middleware/policy layer:

- `auth.py`
- `policies.py`

Error layer:

- `errors.py`

## Dependency Policy

R002 has no runtime package dependencies.

R002 must remain independent of downstream repositories. Downstream exchange,
market-data, dataset, or application requirements must not silently redefine
R002 scope.

## Public / Private Module Boundary

The observed package-root public API is:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

Middleware, authentication, retry, rate limiting, mock transport, and errors
are observed implementation modules and require explicit review before any
public API freeze.

## Transport-Neutral Runtime Model

`HttpRuntime` orchestrates execution. `Transport` owns request execution.
Middleware owns behavior. Boundary objects carry data.

The runtime must not contain exchange-specific, market-data-specific, or
application-specific logic.

## Middleware / Auth / Policy Boundary

Authentication, retry, and rate limiting are implemented as middleware/policy
behavior, not as runtime responsibilities.

These components are internal unless explicitly approved as public API.

## Validation Expectations

Request, response, and settings objects should validate structural invariants at
construction. Invalid boundary data should fail fast.

## Error-Handling Expectations

Repository-native HTTP errors should preserve original exception context when
normalizing transport or middleware failures.

## Known Incomplete Or Deferred Capabilities

R002 does not currently ship a concrete live HTTP transport.

Real network transport implementations are out of scope unless separately
approved.

Response decoding helpers are not observed and should remain out of scope
unless separately approved.

## Evidence Limitations

This design is recovered from observed source, tests, metadata, and stale
documentation. Source and tests are evidence of implementation, not approval.

This document does not approve R002, freeze R002, freeze the API, assign Release
Phase, approve milestones, or declare release readiness.
