# MCP-SWTR community runtime provenance

- Original repository: MCP-SWTR (corporate GitVerse; user-approved for public source publication)
- Original GitVerse source commit: `ea7f75f2b2f21fab0d3a262b2494a48309892cab` (2026-08-25).
- Sanitized Review source commit: `c91f8ed1637092898cc407e1dc870df42e6ae20f`.
- Distribution: **Python runtime only** (server, models, requirements, safe Docker context, env template).
- The optional Node/npx runtime and `api-docs.json` are omitted because they are not needed for the community Task API's stdio/SSE route.
- Sanitization relative to Review: only example AS21 space/task identifiers in MCP tool descriptions changed to generic PAY/CRM examples; package author email replaced with `redacted@example.invalid`. Core MCP request/response behavior is unchanged.
- No GitVerse commit history, user-specific configuration, credentials or local `.env` files included.
- For future updates, take a vetted source snapshot and repeat secret/PII scans before public release.
