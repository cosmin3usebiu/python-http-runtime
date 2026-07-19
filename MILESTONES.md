# R002 Milestones: python-http-runtime

## Status

This document records observed implementation state for documentation
alignment. It does not approve milestones, freeze artifacts, assign Release
Phase, validate builds, or declare release readiness.

R002 remains unapproved, unfrozen, API not frozen, and not in Release Phase.

## Observed Implementation Areas

### Repository Structure

Observed:

- package layout
- tests
- docs and examples directories
- CI workflow
- packaging metadata
- `py.typed`

### Core Object Model

Observed:

- package-root exports limited to five objects
- request, response, settings, runtime, and transport modules
- repository-native errors

### Request / Response / Settings Models

Observed:

- immutable `HttpRequest`
- immutable `HttpResponse`
- immutable `RuntimeSettings`
- structural validation
- header, body, query parameter, and timeout normalization

### Transport Contract and Mock Transport

Observed:

- one-method `Transport` contract
- deterministic `MockTransport`
- request recording
- response request rebinding
- transport error normalization

### Runtime Orchestration

Observed:

- `HttpRuntime`
- effective request construction
- base URL handling
- default header merging
- timeout resolution
- middleware pipeline execution
- transport delegation
- return-type validation

### Middleware Policies

Observed:

- generic auth/header middleware
- retry middleware
- rate-limit middleware

Middleware behavior is policy behavior. It is not owned by the runtime
orchestrator.

### Error Normalization

Observed:

- package-level error hierarchy
- middleware failure normalization
- transport failure normalization
- invalid collaborator return-type handling

### Documentation Remediation

Current:

- skeleton-only documentation language has been removed
- API boundary disposition has been documented
- live HTTP transport absence has been documented as a non-goal

## Non-Approved Capabilities

No live HTTP transport milestone is approved or implemented.

The following remain outside current R002 scope unless separately approved:

- `requests` transport
- `httpx` transport
- `aiohttp` transport
- urllib transport
- response decoding helpers
- exchange-specific signing
- downstream domain integrations

## Remaining Governance Work

Future work may include:

- read-only documentation verification
- build/sdist/wheel validation proposal
- governance reassessment
- explicit API freeze review
- release-readiness review

None of those activities are started or approved by this file.
