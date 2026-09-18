# Codex integration

Open-source Testamur integration for Codex-style coding agents.

Responsibilities:

- translate agent/tool activity into explicit Testamur capture events
- preserve WorkSession boundaries
- record exposure without silently asserting reliance
- hand reconciliation back to Testamur core
- remain inspectable and distributable independently of the hosted product

This integration must not contain hosted credentials, billing, private tenant logic, or a second Testamur semantic implementation.
