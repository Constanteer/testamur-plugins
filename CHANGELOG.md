# Changelog

## v1.1.0

This release advances the Codex integration without changing Testamur's semantic firewall.

### Added

- Project-aware MCP operations for immutable supply-chain scan/read/diff and advisory revalidation.
- Project-scoped advisory assessment writes that accept evidence/provenance but not caller-supplied verdict/state/trust scores.
- Repository-binding lifecycle MCP tools for inspecting, enabling/disabling, and non-destructively unbinding scanner inputs.
- Host-neutral MathHub MCP launcher alongside the Testamur Source Gateway.
- First-run doctor checks for the canonical project/repository-binding MCP surface and MathHub availability.
- Existing-project first-use documentation covering Scan → Compare → Impact → Revalidation.

### Preserved boundaries

- `recorded != verified`
- `fetched != relied`
- `changed != invalid`
- `stale != false`
- `EXPOSED_TO_MODEL != RELIED`
- exact candidate / lineage evidence is not an affectedness verdict
- no generic trust score

### Release operator note

The existing annotated `v1.0.0` tag points at the initial package commit and must not be moved. Publish `v1.1.0` from this release commit after package checks have actually executed, or after their infrastructure-not-executed state has been explicitly recorded. Create the corresponding published GitHub Release object; a tag without a GitHub Release does not satisfy Testamur's public distribution contract.
