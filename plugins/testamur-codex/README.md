# Testamur for Codex

Testamur for Codex captures inspectable agent provenance and gives Codex access to the local Testamur Source Gateway.

It adds two things:

1. lifecycle hooks capture **observable** WorkSession/tool events;
2. a local MCP server exposes exact source/revision operations.

It intentionally does **not** capture hidden model reasoning and does not turn exposure/fetch into durable reliance.

## Install

The plugin depends on an installed Testamur core package. Confirm both executables are available to Codex:

```bash
command -v testamur
command -v testamur-gateway-mcp
```

`testamur-gateway-mcp` is a stdio server, so let Codex start it through the bundled MCP declaration.

Add this repository as a plugin marketplace:

```bash
codex plugin marketplace add Constanteer/testamur-plugins
```

Then install **testamur-codex** from that marketplace in the Codex plugin manager.

For a reproducible setup, pin the marketplace to a GitHub release tag or exact commit.

## What it records

The hook adapter records observable lifecycle/tool events into Testamur-owned state. The bundled MCP launcher exposes `testamur.source_gateway_mcp`.

The package preserves the Testamur semantic firewall:

```text
recorded != verified
fetched != relied
changed != invalid
stale != false
lineage != affectedness verdict
```

## State

By default the plugin resolves state under the Testamur-owned home directory.

- `TESTAMUR_HOME` changes the Testamur state root.
- `TESTAMUR_DB` explicitly overrides the database path.

Host-specific plugin data directories are not treated as the durable Testamur database.

## Verify

Start a fresh Codex session after installation and try:

> Fetch this documentation through Testamur and preserve the exact revision used.

Then:

> Show what observable provenance Testamur captured for this session.

A fetched source must not automatically become a durable reliance.

## Package layout

```text
.codex-plugin/plugin.json  native Codex plugin manifest
hooks/hooks.json           lifecycle hook registration
hooks/capture.py           hook bootstrap
.mcp.json                  bundled local MCP declaration
mcp/serve.py               MCP bootstrap
```

## Release source

GitHub Releases in this repository are the version/distribution source of record. Marketplace installation should resolve back to an inspectable release/tag.

See the repository root README for Claude Code, OpenCode, generic MCP setup, upgrade guidance and troubleshooting.

## Publication status

The current package is suitable for repository marketplace distribution. Public directory submission remains a separate publication step; do not invent hosted OAuth or remote-MCP metadata for this local plugin.

See `SUBMISSION.md` and `submission-tests.json` for the submission checklist and semantic test cases.
