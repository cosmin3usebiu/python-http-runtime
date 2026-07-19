# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

- Refreshed documentation to describe the current transport-neutral HTTP runtime
  implementation.
- Documented the package-root public API boundary:
  `HttpRuntime`, `HttpRequest`, `HttpResponse`, `RuntimeSettings`, and
  `Transport`.
- Documented public submodule API candidates for errors, authentication
  middleware, policy middleware, and `MockTransport`.
- Documented middleware extension/support contracts as public but explicitly
  non-frozen/deferred.
- Documented internal-only implementation details by exclusion.
- Documented that R002 does not ship a concrete live HTTP transport.

This changelog entry does not declare a release version, release date, API
freeze, Release Phase assignment, build validation, publication readiness, or
live HTTP validation.
