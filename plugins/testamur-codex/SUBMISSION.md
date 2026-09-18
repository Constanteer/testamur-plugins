# OpenAI plugin submission preparation

Status: **assets prepared; public submission intentionally not yet enabled**.

The current Testamur Codex plugin can be tested through a repository/local marketplace. Public directory publication should happen from the dedicated `testamur-plugins` repository after the public site/domain and publisher identity are ready.

## Listing draft

- **Name:** Testamur
- **Category:** Productivity
- **Short description:** Preserve what Codex work depended on.
- **Long description:** Capture observable agent/tool provenance as Testamur WorkSessions and route exact source access through the Testamur Source Gateway, while keeping exposure distinct from durable reliance and excluding hidden model reasoning.
- **Developer:** Constanteer
- **Website:** fill with the final public Testamur site URL after `testamur-site` is deployed
- **Support URL:** fill with the dedicated public support route/address
- **Privacy URL:** final public URL for the privacy page extracted from `site/privacy.html`
- **Terms URL:** final public URL for the terms page extracted from `site/terms.html`

Do not submit placeholder URLs.

## Starter prompts

1. “Track the sources this coding session actually depends on and show me what would need revalidation if one changes.”
2. “Fetch this documentation through Testamur and preserve the exact revision used.”
3. “Show the provenance captured for this session without treating every tool result as relied upon.”
4. “Which watched sources changed, and which downstream work may need review?”
5. “Explain why this result is marked stale without calling it false.”

## Submission shape decision

### Local/repository marketplace

Current package shape is valid for development:

```text
hooks -> local Testamur core
MCP launcher -> local Testamur Source Gateway
```

### Public directory: remote MCP route

Before selecting an MCP-containing public submission:

- deploy the MCP server to a stable public HTTPS endpoint;
- use the final Testamur domain and complete any required domain verification;
- define production authentication/authorization if the endpoint accesses private user state;
- ensure every exposed tool has correct safety/behavior annotations;
- ensure no tool equates fetched/exposed content with durable reliance;
- publish final Website, Support, Privacy and Terms URLs.

The local `python3 mcp/serve.py` launcher is not the public endpoint.

### Public directory: skills-only route

A skills-only submission is possible only after the plugin contains a useful self-contained Testamur skill. Do not label the current hook/MCP package “skills-only”; no public submission should misrepresent the package shape.

## Publisher/account prerequisites

Before submission:

- select the verified developer/publisher identity that should appear publicly;
- ensure the submitting OpenAI Platform organization/user has the required plugin-management permission;
- decide the countries/regions where the plugin should be offered;
- complete policy/compliance attestations in the submission portal.

These are portal/account operations and are intentionally not encoded in repository secrets.

## Test cases

Canonical draft cases are in `submission-tests.json`.

They are written around semantic behavior rather than exact prose so host/model wording can vary without weakening the Testamur invariants.

## Publication gate

Do not submit until all are true:

- [ ] dedicated public plugin repository exists;
- [ ] plugin installs from that repository marketplace;
- [ ] Testamur core dependency is documented and installable;
- [ ] final public website/support/privacy/terms URLs exist;
- [ ] marketplace authentication policy matches the actual runtime;
- [ ] public submission shape is chosen (skills-only or remote MCP);
- [ ] if MCP: stable HTTPS endpoint is deployed and verified;
- [ ] positive/negative submission cases pass;
- [ ] publisher identity is verified;
- [ ] no placeholder URL or private transition-repository link remains.
