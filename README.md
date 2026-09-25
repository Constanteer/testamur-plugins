# Testamur Plugins

Official integrations for Testamur.

This repository contains thin host adapters that connect coding agents and developer tools to the Testamur provenance, source-revision and revalidation model. The integrations do **not** implement a second Testamur runtime.

- **Testamur:** https://testamur.org
- **Core repository:** https://github.com/Constanteer/testamur
- **Hosted integrations page:** https://testamur.org/integrations

## Available integration

### Codex

The native Codex plugin lives at:

```text
plugins/testamur-codex/
```

It provides:

- lifecycle hooks for observable session/tool activity;
- local MCP launchers for the Testamur Source Gateway and MathHub;
- a packaged MathHub-first proof-obligation skill for search/reuse/import/prove/build workflows;
- a declarative `github_branch` monitor provider.

It does not capture hidden model reasoning and it does not turn source exposure into durable reliance.

### Distribution status

The Codex plugin is available from this GitHub repository and is intended to be installed from an inspectable release/tag or exact revision.

It is **not currently listed in Codex's host-operated marketplace or other third-party plugin marketplaces**. The maintainer is under 18 and cannot yet complete some publisher/account eligibility steps required for those listings. This is a distribution and discovery limitation, not a runtime limitation: the plugin, hooks, MCP launchers and Testamur integration are usable directly from this repository.

GitHub Releases are the canonical reproducible distribution boundary until host-operated marketplace listings become available.

## 5-minute first run

Use one environment for Testamur core, the plugin doctor, and the Codex process. The shortest launch path is:

```bash
# 1. Confirm Testamur core and the MCP gateway are visible.
command -v testamur
command -v testamur-gateway-mcp

# 2. From this repository, validate host wiring.
python plugins/testamur-codex/scripts/doctor.py

# 3. Add this GitHub repository as a Codex marketplace source.
codex plugin marketplace add Constanteer/testamur-plugins
```

Install **testamur-codex** from that repository-backed marketplace source, then start a **fresh Codex session from the same environment**. In the fresh session, ask Codex to fetch a documentation source through Testamur and preserve the exact revision used. Inspect the resulting observable provenance before adding any durable reliance claim. For mathematical work, try a task that depends on a nontrivial invariant or equivalence: the packaged skill should search MathHub first, reuse/import existing Lean-checked mathematics when possible, and require a canonical Lean Build before reporting a generated proof as verified.

The first run has three deliberately separate facts:

1. **Fetched / exposed** — the host can record that a source revision crossed the model boundary.
2. **Relied** — durable reliance is recorded only when the workflow explicitly establishes it; exposure alone is not reliance.
3. **Revalidated** — a later review can record a new judgment against a changed or stale revision; change/staleness is not itself invalidity or falsity.

If the doctor is not ready, fix the reported environment wiring before debugging provenance semantics. A successful doctor proves installation wiring only; it does not verify a source.

## Prerequisite

Install Testamur core first and make sure these commands are available in the environment used by your host:

```bash
command -v testamur
command -v testamur-gateway-mcp
```

The core runtime is maintained in `Constanteer/testamur`.

## Check the launch environment

The plugin and Testamur core must be visible from the **same environment that launches Codex**. From a checkout of this repository, run:

```bash
python plugins/testamur-codex/scripts/doctor.py
```

A successful doctor ends with `Ready: start a fresh Codex session from this environment.` It checks the installed Testamur core, the project/repository-binding MCP surface, the bundled plugin files, and the separate MathHub MCP surface declared by the plugin. If Testamur core is missing, install/activate it in the Codex environment. If MathHub is not importable and `mathhub-mcp` is not on `PATH`, install the MathHub client surface or set `MATHHUB_ROOT` to a MathHub checkout before starting a fresh Codex task.

The doctor checks installation wiring only. Availability does not verify a source or mathematical claim, and it does not turn fetched/exposed material into reliance.

## Install the Codex plugin

Because there is no host-operated marketplace listing yet, add this GitHub repository directly as a Codex marketplace source:

```bash
codex plugin marketplace add Constanteer/testamur-plugins
```

Then install **testamur-codex** from that source.

For reproducible environments, use a published GitHub Release/tag or exact commit instead of following the mutable default branch. A future host-operated marketplace listing should remain traceable back to the same inspectable release.

## Verify

After the doctor reports ready, start a **fresh Codex session from that same environment** and try a source-provenance workflow such as:

> Fetch this documentation through Testamur and preserve the exact revision used.

Then inspect the observable provenance captured for the session.

For mathematical proof obligations, the packaged skill preserves a second boundary: a MathHub Claim, graph edge, or registered Proof candidate is not itself verification; canonical Lean-backed Build evidence determines formal proof status.

The integration preserves the Testamur semantic boundary:

```text
recorded != verified
fetched != relied
changed != invalid
stale != false
EXPOSED_TO_MODEL != RELIED
lineage != affectedness verdict
```

## Other MCP clients

Claude Code, OpenCode and other MCP-capable hosts can use the core stdio server directly:

```text
testamur-gateway-mcp
```

Host-specific wrappers should add lifecycle or UX integration without forking Testamur's state or semantics. For MCP-only onboarding, first run the gateway directly in the same environment to distinguish transport/setup failures from host-adapter failures; then configure the client to launch that same command.

## Repository layout

```text
.agents/plugins/marketplace.json     Codex marketplace manifest
plugins/testamur-codex/              native Codex plugin
tests/                               repository-level package tests
```

The `.agents/plugins/marketplace.json` file is part of the distribution surface and is intentionally committed.

## State

Integrations use Testamur-owned state:

- `TESTAMUR_HOME` selects the Testamur state root.
- `TESTAMUR_DB` overrides the database path.

Host-only plugin data directories are not treated as the durable Testamur database.

## Development

Run the plugin package tests from the repository root:

```bash
python -m pytest -q
```

The package-level documentation in [plugins/testamur-codex/README.md](plugins/testamur-codex/README.md) contains implementation details and verification notes.

## Releases

The initial annotated tag is **v1.0.0**. Current `main` prepares **v1.1.0**, which adds the Project supply-chain/advisory MCP surface, host-neutral MathHub MCP, repository-binding lifecycle tools, and stricter first-run doctor checks.

GitHub Releases are the reproducible distribution boundary for this repository. Host-operated marketplace listings are not currently available for this project because of the maintainer's age/account eligibility constraints; when they become available, they should remain a discovery/install layer over the same inspectable GitHub release rather than a separate authority.

## Maintainer and development note

This project is maintained by a full-time student alongside school and exams. During high-pressure academic periods, responses to issues, pull requests, and marketplace work may be slower.

AI tools have been used extensively for implementation, integration work, tests, documentation, and review. The maintainer remains responsible for architecture, release decisions, and the published package. AI output is not treated as proof that an integration is correct or safe; the repository keeps executable tests, doctor checks, inspectable source, and release-pinned distribution paths for that reason.

## License

Testamur Plugins is licensed under the [Apache License 2.0](LICENSE).
