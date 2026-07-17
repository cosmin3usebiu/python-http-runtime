# R002 Milestones: python-http-runtime

## Status

This is a recovered draft proposal based on observed implementation evidence.
It does not approve or freeze R002.

R002 approval/freeze state remains unverified. The API is not frozen. Release Phase is not assigned.

Milestone approval is not granted by this file. Observed code and tests are
evidence only.

No milestone is approved or frozen by this file.

## Proposed Milestone 1: Repository Skeleton

Observed evidence:

- Packaging metadata.
- CI workflow.
- Documentation and example directory structure.
- Source and test package layout.
- `py.typed`.

Acceptance criteria:

- Package is importable.
- Standard repository structure exists.
- No runtime behavior required.

Status:

- Appears implemented based on observed files.
- Not approved.

## Proposed Milestone 2: Core Package Structure

Observed evidence:

- Public package root.
- Error hierarchy.
- Transport contract module.
- Runtime/settings/request/response module boundaries.
- Tests for repository structure.

Acceptance criteria:

- Minimal package-root exports.
- Internal modules importable.
- No broad public API expansion.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 3: Request / Response / Settings Models

Observed evidence:

- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- Request/response/settings tests.

Acceptance criteria:

- Immutable boundary objects.
- Header normalization.
- Query parameter normalization.
- Body normalization.
- Timeout validation.
- Structural response validation.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 4: Transport Contract and Mock Transport

Observed evidence:

- `Transport`
- `MockTransport`
- Transport contract tests.
- Mock transport tests.

Acceptance criteria:

- One-method transport contract.
- Deterministic mock transport.
- Request recording.
- Transport error normalization.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 5: Runtime Orchestration

Observed evidence:

- `HttpRuntime`
- `ExecutionContext`
- `compose_middleware`
- Runtime tests.

Acceptance criteria:

- Runtime builds effective requests.
- Runtime merges default settings.
- Runtime delegates to middleware.
- Runtime delegates execution to transport.
- Runtime validates response type.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 6: Middleware Policies

Observed evidence:

- Authentication middleware.
- Bearer token middleware.
- Basic auth middleware.
- API key header middleware.
- Custom header injection middleware.
- Retry middleware.
- Rate-limit middleware.
- Auth and policy tests.

Acceptance criteria:

- Middleware modifies execution through request copies.
- Retry handles transport failures.
- Rate limiting uses injectable sleep/clock behavior.
- Invalid policy configuration fails fast.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 7: Error Normalization

Observed evidence:

- `HttpRuntimeError`
- `HttpConfigurationError`
- `HttpTransportError`
- `HttpTimeoutError`
- `HttpResponseError`
- `HttpMiddlewareError`
- Error tests.

Acceptance criteria:

- Unknown middleware failures are wrapped.
- Unknown transport failures are wrapped.
- Normalized HTTP errors propagate.
- Invalid collaborator return values fail fast.

Status:

- Appears implemented based on observed source/tests.
- Not approved.

## Proposed Milestone 8: Documentation and Release Recovery

Observed evidence:

- README, docs, and examples still contain skeleton or placeholder language.

Acceptance criteria:

- README reflects observed implementation.
- API documentation reflects approved API.
- Examples demonstrate approved usage.
- Release notes and changelog align with approved scope.

Status:

- Incomplete.
- Not approved.

## Recovery Status

Proposed milestones 1-7 appear implemented based on observed source/tests but
are not approved.

Proposed milestone 8 is incomplete because documentation and examples remain
stale or placeholder-level.

No milestone is approved or frozen by this file.

No live transport milestone is approved by this file.
