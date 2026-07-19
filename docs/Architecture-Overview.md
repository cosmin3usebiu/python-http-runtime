# Architecture Overview

R002 is a transport-neutral HTTP runtime.

```text
HttpRequest
    |
    v
HttpRuntime
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

The runtime orchestrates execution. Middleware owns behavior. Transport owns
request execution. Request, response, and settings objects are boundary data.

## Boundaries

- `HttpRequest` defines outbound request data.
- `HttpResponse` defines raw response data.
- `RuntimeSettings` defines runtime defaults.
- `HttpRuntime` coordinates the execution pipeline.
- `Transport` executes requests.
- Auth, retry, and rate-limit middleware apply policy behavior.
- `MockTransport` supports deterministic tests and examples.

## Non-Goals

R002 does not provide concrete live transports, response decoding helpers,
exchange signing, market-data behavior, persistence, trading, or strategy
logic.

R002 is not approved, frozen, in Release Phase, or release-ready.
