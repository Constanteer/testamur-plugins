# Testamur Codex plugin

This package connects Codex-style agent activity to an installed Testamur core.

It does two things:

1. lifecycle hooks capture observable WorkSession/tool events;
2. a local MCP launcher exposes the Testamur Source Gateway.

It intentionally does **not** capture hidden model reasoning and does not turn exposure/fetch into durable reliance.

## Runtime dependency

The plugin does not vendor Testamur core.

The environment running the plugin must provide an importable `testamur` package with:

- `testamur.codex_gateway_hook`
- `testamur.source_gateway_mcp`

The plugin launchers first import the installed package. Their monorepo-relative lookup is a development fallback only and should not be treated as the distribution contract after repository extraction.

## Local / repository marketplace

The transition repository already includes a repository marketplace entry under:

```text
.agents/plugins/marketplace.json
```

After extraction to the dedicated plugin repository, keep that catalog in the new repository so developers can add the repo as a Codex marketplace source.

The marketplace policy fields still need a deliberate authentication choice before treating the catalog as publication-ready. The current plugin has local hooks/MCP and no hosted OAuth contract; do not invent an authentication flow merely to satisfy metadata.

## Public directory status

The current package is suitable for local/repository marketplace testing.

A public OpenAI Plugins Directory submission needs a deliberate submission shape:

- **skills-only**, if Testamur ships a useful workflow without a remote service; or
- **MCP**, after Testamur exposes a stable public HTTPS MCP endpoint.

The existing `.mcp.json` launches a local Python process. That local process is not itself the remote HTTPS MCP endpoint required for a public MCP submission.

See `SUBMISSION.md` and `submission-tests.json`.
