# R002 Decisions: python-http-runtime

## Status

This is a recovered draft proposal based on observed implementation evidence.
It does not approve or freeze R002.

R002 approval/freeze state remains unverified. The API is not frozen. Release Phase is not assigned.

All decisions in this file are proposed and unapproved unless explicitly stated
otherwise.

## Decisions To Ratify

### DEC-R002-001: R002 Owns HTTP Runtime Orchestration

Decision to ratify:

R002 owns generic HTTP request execution orchestration through runtime,
middleware, and transport contracts.

Evidence:

Observed `HttpRuntime`, `ExecutionContext`, middleware composition, and runtime
tests.

Status:

Proposed, not approved.

### DEC-R002-002: R002 Has No Runtime Dependencies

Decision to ratify:

R002 remains dependency-light and has no runtime package dependencies.

Evidence:

`pyproject.toml` declares an empty dependency list.

Status:

Proposed, not approved.

### DEC-R002-003: Transport Is The Primary Extension Point

Decision to ratify:

`Transport` is the public extension point for request execution.

Evidence:

Observed public `Transport` export and runtime delegation.

Status:

Proposed, not approved.

### DEC-R002-004: Runtime Orchestrates But Does Not Own Policy Behavior

Decision to ratify:

Retry, rate limiting, and authentication behavior belong to middleware/policy
components, not the runtime core.

Evidence:

Observed `auth.py`, `policies.py`, and runtime middleware composition.

Status:

Proposed, not approved.

### DEC-R002-005: R002 Does Not Ship A Live HTTP Transport

Decision to ratify:

R002 defines the transport contract and deterministic mock transport behavior
but does not ship a concrete live network transport.

Evidence:

Observed `Transport` and `MockTransport`; no requests/httpx/aiohttp transport
module observed.

Status:

Proposed, not approved.

### DEC-R002-006: Public API Remains Minimal

Decision to ratify:

The package-root public API should remain limited to core runtime concepts
unless an expansion is explicitly approved.

Evidence:

Observed `__all__` exports exactly five objects and repository tests assert
minimal public exports.

Status:

Proposed, not approved.

## Open Decisions

- Whether `MockTransport` should become public API or remain internal testing
  support.
- Whether repository-native HTTP error classes should become public API.
- Whether auth middleware should remain internal or become public extension API.
- Whether retry and rate-limit middleware should remain internal or become
  public extension API.
- Whether a concrete live transport belongs in R002 or a separate repository.
- Whether R002 should enter Release Phase after artifact recovery or require
  code work.

## Evidence Limitations

Source and tests provide implementation evidence. They do not prove prior
approval, API freeze, milestone approval, or release readiness.

This file does not approve R002, freeze R002, freeze the API, assign Release
Phase, approve milestones, or declare release readiness.
