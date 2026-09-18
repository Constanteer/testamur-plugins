# Testamur plugins

Testamur integrations put source provenance and change/revalidation information inside coding-agent workflows.

**Status:** staging repository for the first public plugin release. GitHub Releases in this repository are the distribution/version source of record. Marketplaces are optional install/discovery layers.

## Requirements

Install Testamur core first and confirm these executables are on the host's PATH:

```bash
command -v testamur
command -v testamur-gateway-mcp
```

`testamur-gateway-mcp` is a stdio MCP server; start it through an MCP host rather than running it interactively.

## Codex — native plugin

Once this repository is published, add it as a Codex marketplace:

```bash
codex plugin marketplace add Constanteer/testamur-plugins
```

Then install **testamur-codex** from the Codex plugin manager.

The native package captures observable lifecycle/tool activity and exposes the local Testamur Source Gateway. It does not capture hidden model reasoning.

For reproducible environments, pin the marketplace to a GitHub release tag or exact commit rather than following a mutable branch.

## Claude Code — MCP route

```bash
claude mcp add --transport stdio testamur -- testamur-gateway-mcp
claude mcp list
```

A native Claude wrapper can add host-specific skills/hooks later without changing the Testamur gateway or evidence model.

## OpenCode — MCP route

```bash
opencode mcp add testamur -- testamur-gateway-mcp
opencode mcp list
```

A native OpenCode package can add host lifecycle behavior later without forking Testamur semantics.

## Other MCP clients

Configure a local stdio MCP server whose command is:

```text
testamur-gateway-mcp
```

## Semantic boundaries

Every integration must preserve:

```text
recorded != verified
fetched != relied
changed != invalid
stale != false
lineage != affectedness verdict
```

## First prompts

- “Track the sources this coding session actually depends on and show me what would need revalidation if one changes.”
- “Fetch this documentation through Testamur and preserve the exact revision used.”
- “Which watched sources changed, and which downstream work may need review?”
- “Explain why this result is stale without treating stale as false.”

## Release model

A GitHub release tag is the version boundary. Release notes should say what changed, and release assets/source should make the installed artifact inspectable.

For reproducible environments, pin a release tag or exact commit rather than following a mutable branch.

## Troubleshooting

**The host cannot start `testamur-gateway-mcp`.** Confirm Testamur core is installed in the same PATH/environment used by the host.

**The server starts but tools do not appear.** Use the host's MCP status/list command and inspect its process error.

**Codex state is somewhere unexpected.** Check `TESTAMUR_HOME` and `TESTAMUR_DB`.

**A dependency changed. Is downstream work automatically invalid?** No. Testamur records change and affectedness/revalidation evidence; `changed != invalid`.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/testamur-codex/
```

The host-specific package stays thin. Testamur core and the Source Gateway remain the semantic authority.
