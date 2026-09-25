---
name: mathhub-proof-workflow
description: Use MathHub when a Codex task needs to establish, check, or materially rely on a nontrivial mathematical claim, theorem, invariant, equivalence, derivation, or proof obligation. Search the read-only Mathlib library and dependency graph before constructing new mathematics; add user-provided Lean only when new source is needed; create and build a new proof only when needed. Do not trigger for routine arithmetic, syntax-only edits, ordinary typechecking, or facts better established by normal tests.
---

# MathHub-first proof workflow

Use this workflow when mathematical correctness is part of the task, including direct proof requests and coding work whose correctness depends on a theorem-like claim.

## Trigger boundary

Treat a proof obligation as material when at least one of these is true:

- the user explicitly asks to prove, formally verify, derive, or check a mathematical statement;
- an implementation or refactor depends on a non-obvious invariant, equivalence, preservation property, bound, identity, convergence claim, or algebraic transformation;
- you are about to rely on a mathematical proposition as a premise for code, design, optimization, numerical work, or a research conclusion;
- a generated proof should be reusable or independently inspectable.

Do not invoke this workflow merely for:

- routine arithmetic;
- obvious syntactic rewrites;
- ordinary compiler/typechecker facts;
- unit-test behavior that is better established by running the tests;
- incidental mathematical language that is not a correctness dependency.

## Workflow

1. **Formulate the obligation.**
   State the mathematical claim precisely enough to search for it. Preserve the user's intended scope and assumptions. Do not weaken a claim just to find a match.

2. **Search the existing mathematics before constructing a proof.**
   Search recorded Claims with `mathhub_search_claims` when durable MathHub records may already exist.
   Search the installed read-only Mathlib library with `mathhub_browse_library` when the theorem may simply already be present upstream.
   - Mathlib is already part of MathHub's library substrate; finding a theorem there is not an import/add operation.
   - Prefer one precise namespace/query when possible.
   - A recorded Claim, a library theorem, and a successful Build are distinct facts.

3. **Open the theorem and walk dependencies directly.**
   Use `mathhub_read_theorem` for the mathematical/source presentation.
   Use `mathhub_read_dependencies` for direct Lean declaration/proof dependencies.
   When several visible dependency nodes are likely to be traversed, call `mathhub_prefetch_dependencies` once for that bounded frontier instead of making the user or agent wait for one inspect per step.
   Dependency arrows mean dependent -> dependency; module ownership is not a dependency edge.

4. **Inspect durable Claim evidence only when that layer matters.**
   If a matching recorded Claim exists, call `mathhub_read_claim`.
   Use `mathhub_read_argument`, `mathhub_read_graph`, or `mathhub_find_path` only when recorded Claim/Proof route evidence is relevant.
   A library theorem does not need to be materialized as a Claim merely to browse, understand, or follow its Lean dependencies.

5. **Reuse existing mathematics when it actually matches.**
   If the theorem exists in Mathlib, use the library theorem directly for discovery and dependency traversal.
   If an existing Claim has a successful canonical Lean-backed Build for the required statement and environment, that Build is the durable MathHub verification evidence.
   Do not treat graph adjacency, registration, source presence, or a human-readable presentation as equivalent to a successful Build.

6. **Materialize an existing Lean theorem only for a real workspace-record need.**
   `mathhub_import_declaration` and `mathhub_import_closure` are advanced compatibility/materialization operations. Do not use them as the normal way to "open" Mathlib.
   Use them only when the task specifically needs a durable Claim/Proof/Build record for an already-existing declaration.
   Keep closure expansion explicitly bounded.

7. **Add new Lean only when new source is being contributed.**
   Use `mathhub_add_lean_source` for user-provided Lean text or a public source URL. This is the Add Lean path.
   Existing Mathlib theorems are already in the library and should not be re-added just to inspect them.

8. **Create a new Claim only when needed.**
   If no suitable existing or importable theorem matches and formal verification is appropriate:
   - call `mathhub_register_claim` with the exact statement/formal declaration and useful metadata;
   - construct a Proof candidate;
   - call `mathhub_register_proof`;
   - call `mathhub_build_proof`.

   Do not fill MathHub with disposable scratch lemmas unless they are necessary to establish the material claim or have independent reuse value.

9. **Let Lean decide the proof result.**
   A registered Proof is a candidate. Report it as verified only when the canonical MathHub Build records success.
   If the build fails, is unavailable, or the environment is mismatched, preserve that status explicitly. Never rewrite failure into success from model judgment.

10. **Preserve Testamur semantic boundaries.**
   MathHub owns Claim / Proof / ProofDependency and Lean-backed mathematical verification.
   Testamur owns observable provenance, source revisions, explicit reliance, revalidation, and downstream impact workflows.
   Keep these invariants:
   - recorded != verified
   - fetched != relied
   - EXPOSED_TO_MODEL != RELIED
   - changed != invalid
   - stale != false
   - graph lineage != verification or affectedness verdict

   Querying or reading a MathHub object does not by itself create durable Testamur reliance. Durable reliance remains an explicit reconciliation decision.

## Response behavior

When MathHub materially affects the answer, report the relevant Claim / Proof / Build identities and the actual Build status when available. Distinguish:

- reused an existing Mathlib theorem for read-only mathematics/dependency traversal;
- reused an existing verified Claim;
- materialized an existing Lean declaration because a durable workspace record was actually required;
- added new user-provided Lean source;
- newly registered Claim with successful Build;
- proof candidate not yet verified;
- failed or unavailable Build.

Do not emit a generic trust score and do not describe a Claim as proved merely because it exists in MathHub.
