# Configuration

R002 configuration is represented by `RuntimeSettings`.

`RuntimeSettings` stores:

- optional `base_url`
- default headers
- optional default timeout

`HttpRequest` may provide a per-request timeout override. The runtime uses the
request timeout when present and otherwise falls back to the runtime default.

R002 does not own configuration loading, profiles, environment variables, or
application configuration files.
