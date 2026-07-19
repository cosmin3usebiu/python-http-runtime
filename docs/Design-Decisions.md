# Design Decisions

## Minimal Root API

The package root exposes only five core objects:

- `HttpRuntime`
- `HttpRequest`
- `HttpResponse`
- `RuntimeSettings`
- `Transport`

Submodule APIs are documented separately to keep the root API small.

## Runtime Is An Orchestrator

`HttpRuntime` coordinates request execution. It does not implement policy
algorithms or concrete network behavior.

## Transport Owns Execution

`Transport` is the primary extension point and has one method:
`execute(request)`.

R002 does not ship live HTTP transports.

## Middleware Owns Policy

Authentication, retry, and rate limiting are middleware concerns. These
behaviors are not embedded in the runtime.

## Extension Contracts Are Deferred

`ExecutionMiddleware`, `ExecutionContext`, `ExecutionHandler`, and
`AuthenticationMiddleware` are public but explicitly non-frozen/deferred.

## Raw Response Boundary

`HttpResponse` stores raw response information. It does not decode JSON, expose
text helpers, or classify status codes.
