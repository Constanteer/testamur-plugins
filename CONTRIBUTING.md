# Contributing to Testamur Plugins

This repository contains official Testamur integrations and packaging surfaces.
The adapters should stay small, inspectable, and subordinate to canonical
Testamur semantics.

## Run the package tests

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

For the Codex plugin, also run the packaged environment doctor from a checkout:

```bash
python plugins/testamur-codex/scripts/doctor.py
```

A doctor failure may simply mean Testamur core is not installed in the same
environment that launches Codex.

## Adapter boundary

Do not implement a second Testamur ontology inside a plugin.

Plugins may:

- translate host lifecycle/tool events into canonical observable events;
- launch the canonical local Source Gateway/MCP server;
- resolve host-specific monitor target configuration;
- provide installation metadata and first-run diagnostics.

Plugins must not:

- infer durable reliance because a model saw or fetched something;
- convert `EXPOSED_TO_MODEL` into `RELIED`;
- create a generic trust score;
- turn `changed` into `invalid`;
- turn advisory/package name or version matches into affectedness;
- own an independent copy of core Source/Revision/Reliance semantics.

If an integration needs a new semantic capability, add it to canonical Testamur
core first and keep the plugin as the adapter.

## Pull requests

Keep host-specific behavior explicit and test the package shape. Changes to the
Codex plugin should preserve the marketplace manifest, hooks, MCP declaration,
monitor-provider manifest, first-run doctor, and release/install documentation.

When adding a new host integration, document:

1. what observable events the host exposes;
2. what the adapter records;
3. what it deliberately does **not** infer;
4. how a user verifies installation in a fresh host session.
