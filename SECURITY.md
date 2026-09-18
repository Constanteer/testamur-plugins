# Security Policy

## Reporting a vulnerability

Please do not publish an undisclosed vulnerability as a public issue.

Use GitHub's private vulnerability-reporting / Security Advisory flow for this
repository when available. A useful report includes:

- plugin/integration version or commit;
- affected host or adapter (Codex hooks, MCP launcher, monitor provider, etc.);
- security impact and realistic preconditions;
- minimal reproduction steps;
- any known mitigation.

Do not attach real credentials, private source content, access tokens, or user
evidence.

If private GitHub reporting is unavailable, use a private maintainer channel
rather than disclosing exploit details publicly.

## Integration security boundaries

Testamur integrations are adapters around the canonical Testamur core. They must
not silently create a second provenance or trust model.

In particular:

- hook/tool observation is not durable reliance;
- `EXPOSED_TO_MODEL != RELIED`;
- `fetched != relied`;
- MCP availability does not mean a source is verified;
- package/advisory identity overlap is not an affectedness verdict;
- plugin failures must not fabricate successful provenance records.

The plugin first-run doctor checks installation wiring only. A successful doctor
does not verify sources or attest to the correctness of downstream work.
