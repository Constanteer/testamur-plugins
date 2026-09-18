# integrations/

Open-source integrations between Testamur and external developer/agent environments live here.

Planned adapters:

- `integrations/codex/`
- `integrations/mcp/`
- `integrations/github/`
- later editor/shell/agent adapters as needed

The integration layer may capture tool/source exposure and produce Testamur WorkSession events, but it must preserve the core invariant:

`EXPOSED_TO_MODEL != RELIED_ON`

Reliance is established only through explicit Testamur reconciliation/policy semantics.

Integrations should remain inspectable and independently distributable from the hosted product.
