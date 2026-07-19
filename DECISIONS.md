# R002 Decisions: python-http-runtime

## Status

This document records documentation-level decisions derived from the current
API boundary disposition.

It does not approve R002, freeze the architecture, freeze the API, assign
Release Phase, validate builds, validate publication readiness, or validate live
HTTP behavior.

R002 remains unapproved, unfrozen, API not frozen, and not in Release Phase.

## Documented Decisions

### DEC-R002-001: R002 Owns HTTP Runtime Orchestration

R002 owns generic HTTP request execution orchestration through
`HttpRuntime`.

The runtime coordinates request execution. It does not own transport
implementation details, middleware policy behavior, exchange behavior, or
downstream domain logic.

### DEC-R002-002: Transport Is The Primary Extension Point

`Transport` is the public execution extension point.

The contract is intentionally small:

```text
execute(HttpRequest) -> HttpResponse
```

Transport lifecycle hooks and concrete client integrations are not part of the
current R002 public contract.

### DEC-R002-003: Package-Root API Remains Minimal

The package-root API remains limited to:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

Submodule-visible objects are documented separately and are not added to the
package root.

### DEC-R002-004: Policy Behavior Belongs In Middleware

Authentication, retry, and rate limiting are middleware/policy behavior. They
are not runtime responsibilities.

The runtime executes the middleware pipeline and delegates behavior to the
middleware objects supplied to it.

### DEC-R002-005: R002 Does Not Ship A Live HTTP Transport

R002 defines the runtime and transport contract only.

It does not ship `requests`, `httpx`, `aiohttp`, or urllib transports. Concrete
live transports require a separate approved design or work package.

### DEC-R002-006: Middleware Extension Contracts Are Deferred

The following objects are public but explicitly non-frozen/deferred:

- `ExecutionMiddleware`
- `ExecutionContext`
- `ExecutionHandler`
- `AuthenticationMiddleware`

They should be documented as extension/support contracts, not final frozen API.

### DEC-R002-007: Internal Composition Details Remain Private

The following objects are internal-only implementation details:

- `compose_middleware`
- `MockTransportOutcome`
- `_bind_request_to_response`

Users should not depend on these objects as public API.

## Non-Claims

These decisions do not imply:

- repository approval
- architecture freeze
- API freeze
- Release Phase assignment
- release readiness
- build artifact validation
- package publication readiness
- production readiness
- security certification
- live HTTP transport support
