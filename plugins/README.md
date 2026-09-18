# Testamur plugins

Testamur integrations put source provenance and change/revalidation information inside coding-agent workflows.

The distribution source of record is the GitHub release stream for:

`Constanteer/testamur-plugins`

The public install page is `plugins.html` in the Testamur site. Marketplaces are optional install/discovery layers; a release tag is the version boundary.

## What you need first

Testamur integrations currently expect the Testamur core package to be installed so these executables are on the host's PATH:

```bash
command -v testamur
command -v testamur-gateway-mcp
```

`testamur-gateway-mcp` is a stdio server, not an interactive CLI; start it through an MCP host rather than running it by itself.

The plugin packages do not vendor the core runtime.

## Monitor-provider boundary

Projects and monitors are owned by Testamur core. A plugin that wants to add a new monitor target type should implement a **monitor target provider**: it receives provider-specific configuration and resolves that configuration to a canonical Testamur Source (by `source_id` or locator). Core then creates the Watch and attaches it to the selected Project.

The Codex integration registers a declarative `github_branch` monitor target provider. It resolves an `owner/repository` plus branch name to that branch's GitHub commits Atom feed; Testamur core still creates the canonical Source and Watch and attaches the Watch to the selected Project. The lifecycle hooks and MCP Source Gateway remain separate capabilities.

## Codex — native plugin

The Codex package adds:

- lifecycle hooks for observable session/tool activity;
- a local MCP Source Gateway;
- the same Testamur state/database contract used by the core CLI.

Add the GitHub repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add Constanteer/testamur-plugins
```

Then install **testamur-codex** from that marketplace in the Codex plugin manager.

For reproducible environments, pin the marketplace to a release tag or exact commit instead of following the default branch.

### Verify

Start a new Codex session and confirm that the Testamur Source Gateway tools are available. Run a small provenance check such as:

> Fetch this documentation through Testamur and preserve the exact revision used.

The plugin must preserve these boundaries:

```text
recorded != verified
fetched != relied
changed != invalid
stale != false
```

It never claims to capture hidden model reasoning.

## Claude Code — MCP route

Until a native Claude Code wrapper is published, use the portable local MCP server:

```bash
claude mcp add --transport stdio testamur -- testamur-gateway-mcp
claude mcp list
```

A native Claude plugin can later add host-specific skills/hooks while keeping the same Testamur gateway and state.

## OpenCode — MCP route

OpenCode can start the same local stdio MCP server:

```bash
opencode mcp add testamur -- testamur-gateway-mcp
opencode mcp list
```

If a native OpenCode package is published later, it should add host lifecycle behavior rather than fork the Testamur provenance model.

## Other MCP clients

Configure a local stdio MCP server whose command is:

```text
testamur-gateway-mcp
```

Environment/state overrides remain owned by Testamur. In particular, `TESTAMUR_HOME` selects the Testamur-owned state root and `TESTAMUR_DB` can point at an explicit database.

## Release and upgrade model

Use GitHub Releases to answer three questions:

1. **What version did I install?** — the release tag.
2. **What changed?** — release notes and the inspectable source diff.
3. **What artifact did I run?** — a release asset, package source, or exact tagged checkout.

Do not rely on an opaque marketplace build as the only version identifier.

When upgrading a pinned environment, read the release notes, update to the intended tag, then verify the host can still see the Testamur MCP tools.

## First prompts

Good smoke tests:

- “Track the sources this coding session actually depends on and show me what would need revalidation if one changes.”
- “Fetch this documentation through Testamur and preserve the exact revision used.”
- “Which watched sources changed, and which downstream work may need review?”
- “Explain why this result is stale without treating stale as false.”

## Troubleshooting

**The host cannot start `testamur-gateway-mcp`.** Confirm the Testamur core package is installed in the same environment/PATH used by the host.

**The MCP server starts but no tools appear.** Use the host's MCP status/list command and inspect the process error before changing Testamur state.

**Codex hooks run but state appears in an unexpected location.** Check `TESTAMUR_HOME` and `TESTAMUR_DB`; the plugin intentionally does not use host-only plugin data as the durable Testamur database.

**A dependency changed. Is everything invalid?** No. Testamur records the change and downstream affectedness/revalidation evidence; `changed != invalid`.

## Development

Current native Codex implementation: `plugins/testamur-codex/`.

Submission/publication preparation remains in:

- `plugins/testamur-codex/SUBMISSION.md`
- `plugins/testamur-codex/submission-tests.json`

Host-specific wrappers should stay thin. The Testamur core and MCP gateway remain the semantic authority.
