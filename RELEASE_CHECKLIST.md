# Testamur plugin launch release checklist

Use this checklist before publishing a Testamur plugin release or linking a release from the hosted/marketing launch path.

## Package integrity

- Run the repository test suite and record the exact commit SHA tested.
- Confirm the packaged plugin manifest, MCP tool names, and install instructions match that commit.
- Confirm the package contains no local credentials, tokens, generated account data, or machine-specific paths.
- Verify the documented Codex/MCP entry point starts from a clean checkout/install.

## Product semantics

A release must preserve the canonical Testamur distinctions:

- `recorded != verified`
- `fetched != relied`
- `changed != invalid`
- `stale != false`
- `EXPOSED_TO_MODEL != RELIED`
- recorded reliance provenance does not itself establish affectedness

Do not add a generic trust score or a plugin-only ontology to simplify onboarding.

## Agent acceptance

From a clean install, exercise the public walkthrough rather than only importing modules:

1. connect the plugin/MCP server;
2. inspect a recorded Source and Revision;
3. compare two revisions;
4. inspect an Impact/review candidate and its recorded basis when available;
5. explicitly revalidate rather than treating change as invalidity;
6. verify unavailable provenance is reported as unavailable rather than inferred from timestamps, current revisions, or ordering.

Where the deterministic evidence demo is available, prefer it so Web, CLI, Codex, and MCP demonstrations share the same evidence flow.

## Release evidence

Before publishing, capture:

- release tag/version;
- source commit SHA;
- test command and observed result;
- package/install smoke result;
- known limitations;
- links used by the hosted app and marketing site.

A CI job that never acquired a runner (`runner_id=0`, empty steps, or equivalent) is infrastructure state. Record it as not executed; do not call the gate green.

## Launch-link gate

Only point public installation UI or launch material at a release after the release exists and the clean-install smoke above has actually executed. Until then, link to repository installation documentation and label it accordingly; do not imply a published release artifact exists.
