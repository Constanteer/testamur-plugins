# Testamur for Codex

Testamur for Codex captures inspectable agent provenance and gives Codex access to the local Testamur Source Gateway and existing-project lifecycle.

It adds three things:

1. lifecycle hooks capture **observable** WorkSession/tool events;
2. a local MCP server exposes exact source/revision operations plus canonical Project supply-chain scan/read/diff and advisory-revalidation operations;
3. a declarative `github_branch` monitor provider lets Testamur Projects add GitHub branch monitors without the plugin owning Watch or Project semantics.

It intentionally does **not** capture hidden model reasoning and does not turn exposure/fetch into durable reliance. Project supply-chain changes are mechanical observations: `changed != invalid`, and advisory candidate lineage is not an affectedness verdict.

## Install

The plugin depends on an installed Testamur core package. Confirm both executables are available to Codex:

```bash
command -v testamur
command -v testamur-gateway-mcp
```

`testamur-gateway-mcp` is a stdio server, so do not use `--help` as a smoke test; let Codex start it through the bundled MCP declaration.

Before installing the marketplace package, run the packaged doctor from this repository checkout:

```bash
python plugins/testamur-codex/scripts/doctor.py
```

The doctor must report that Testamur is importable and both CLI entrypoints are available from the environment that will launch Codex. If it fails, fix the environment and start a fresh Codex task rather than relying on a temporary launcher fallback.

Add the plugin repository marketplace:

```bash
codex plugin marketplace add Constanteer/testamur-plugins
```

Then install **testamur-codex** from that marketplace in the Codex plugin manager.

For a reproducible setup, pin the marketplace to a GitHub release tag or exact commit.

## What it records and exposes

The hook adapter records observable lifecycle/tool events into Testamur-owned state. The bundled MCP launcher prefers the installed core's public `testamur.repository_binding_mcp` surface (the same implementation behind `testamur-gateway-mcp`), then falls back to `testamur.source_gateway_project_mcp` and finally the older source-only gateway for compatibility with older installations. The canonical repository-binding server installs the Project-aware tools and exposes the source tools together with:

- `testamur.project_repository_binding` — inspect the durable repository binding and its scanner-eligibility lifecycle state;
- `testamur.set_project_repository_binding_enabled` — enable or disable scanning without rewriting immutable binding revisions;
- `testamur.project_repository_unbind` — non-destructively disable scanning while preserving binding identity and history;
- `testamur.project_scan` — rescan an explicitly repository-bound existing Project and append an immutable supply-chain observation;
- `testamur.project_supply_chain` — read the current Project supply-chain projection;
- `testamur.project_supply_chain_diff` — compare immutable Project scan observations mechanically, including dependency additions/removals/version transitions;
- `testamur.project_advisory_revalidation` — read Project-scoped advisory review/revalidation work without manufacturing an affectedness verdict;
- the canonical Project-scoped advisory assessment write surface, which records evidence against an exact current candidate rather than accepting an agent-supplied verdict.

The plugin does not reimplement scanning, diffing, affectedness, or Project storage. Those semantics remain owned by the installed Testamur core. Both launchers also register `testamur-monitor-providers.json` into the Testamur-owned provider registry so the hosted/local Web product can expose the GitHub branch monitor type.

The package preserves the Testamur semantic firewall:

```text
recorded != verified
fetched != relied
changed != invalid
stale != false
EXPOSED_TO_MODEL != RELIED
lineage != affectedness verdict
```

No generic trust score is introduced by the plugin or its MCP launcher.

## State

By default the plugin resolves state under the Testamur-owned home directory.

- `TESTAMUR_HOME` changes the Testamur state root.
- `TESTAMUR_DB` explicitly overrides the database path.

Host-specific plugin data directories are not treated as the durable Testamur database.

## Verify

Run the doctor again after installation. Then start a fresh Codex session from the same environment and try:

> Fetch this documentation through Testamur and preserve the exact revision used.

Then:

> Show what observable provenance Testamur captured for this session.

For an existing Project with an explicit repository binding, also try:

> Inspect this Project's repository binding state. If scanning is disabled, explain that this is scanner eligibility only; preserve the binding identity/history and do not treat disabled as invalid, affected, verified, or relied upon.

Then:

> Rescan this Project's supply chain, then compare the new immutable scan with the previous scan. Report additions, removals and version transitions without treating change as invalidity.

Then:

> Show advisory revalidation work for this Project. Keep candidate overlap separate from affectedness, verification and reliance.

A fetched source must not automatically become a durable reliance, and a dependency delta must not automatically become an invalidity or vulnerability verdict.

## Package layout

```text
.codex-plugin/plugin.json  native Codex plugin manifest
hooks/hooks.json           lifecycle hook registration
hooks/capture.py           hook bootstrap
.mcp.json                  bundled local MCP declaration
mcp/serve.py               Canonical repository-binding/Project MCP bootstrap with compatibility fallback
scripts/doctor.py          first-run environment doctor
testamur-monitor-providers.json  declarative monitor provider manifest
```

The launchers import the installed `testamur` package first. Monorepo-relative lookup is a development fallback only.

## Release source

GitHub Releases in `Constanteer/testamur-plugins` are the version/distribution source of record. Marketplace installation should resolve back to an inspectable release/tag.

See the repository-level plugin README for Claude Code, OpenCode, generic MCP setup, upgrade guidance and troubleshooting.

## Publication status

The current package is suitable for local/repository marketplace distribution. Public directory submission remains a separate publication step; do not invent hosted OAuth or remote-MCP metadata for this local plugin.

See `SUBMISSION.md` and `submission-tests.json` for the submission checklist and semantic test cases.
