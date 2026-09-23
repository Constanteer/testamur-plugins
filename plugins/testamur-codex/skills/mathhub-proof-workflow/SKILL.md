---
name: mathhub-proof-workflow
description: Use MathHub when a Codex task needs to establish, check, or materially rely on a nontrivial mathematical claim, theorem, invariant, equivalence, derivation, or proof obligation. Search before proving; reuse or import existing Lean-checked mathematics when possible; create and build a new proof only when needed. Do not trigger for routine arithmetic, syntax-only edits, ordinary typechecking, or facts better established by normal tests.
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

2. **Search MathHub before constructing a new proof.**
   Call `mathhub_search_claims` with the most discriminative mathematical terms, theorem name, or Lean identifier available.
   - Prefer one precise query.
   - If terminology is ambiguous, try a small number of materially different queries.
   - A search hit is only a recorded Claim candidate, not a verification verdict.

3. **Inspect plausible existing Claims.**
   For a plausible result, call `mathhub_read_claim`.
   Use `mathhub_read_argument`, `mathhub_read_graph`, or `mathhub_find_path` only when dependency or proof-route evidence is relevant.
   Check the exact statement, assumptions, formal binding, Proof records, Build state, and environment before relying on it.

4. **Reuse verified mathematics when it actually matches.**
   If an existing Claim has a successful canonical Lean-backed Build for the required statement and environment, reuse it instead of generating a duplicate proof.
   Do not treat graph adjacency, registration, or a human-readable argument as equivalent to Lean verification.

5. **Import an existing Lean theorem when appropriate.**
   If the required theorem already exists in the available Lean environment but is not yet represented as a MathHub Claim, use `mathhub_import_declaration`.
   Use `mathhub_import_closure` only when the dependency closure is useful for the task. Its current host-neutral MCP contract takes plural `declaration_names` so one request can name one or more roots; use `max_depth` and `max_claims` to keep closure expansion explicitly bounded.
   Importing a closure records/imports declarations; it does not itself verify them. Preserve the external declaration identity and use MathHub's canonical Lean-backed Build result for verification status.

6. **Create a new Claim only when needed.**
   If no suitable existing or importable theorem matches and formal verification is appropriate:
   - call `mathhub_register_claim` with the exact statement/formal declaration and useful metadata;
   - construct a Proof candidate;
   - call `mathhub_register_proof`;
   - call `mathhub_build_proof`.

   Do not fill MathHub with disposable scratch lemmas unless they are necessary to establish the material claim or have independent reuse value.

7. **Let Lean decide the proof result.**
   A registered Proof is a candidate. Report it as verified only when the canonical MathHub Build records success.
   If the build fails, is unavailable, or the environment is mismatched, preserve that status explicitly. Never rewrite failure into success from model judgment.

8. **Preserve Testamur semantic boundaries.**
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

- reused existing verified Claim;
- imported existing Lean declaration;
- newly registered Claim with successful Build;
- proof candidate not yet verified;
- failed or unavailable Build.

Do not emit a generic trust score and do not describe a Claim as proved merely because it exists in MathHub.
