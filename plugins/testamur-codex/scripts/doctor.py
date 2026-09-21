from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path


def _plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def inspect_environment() -> dict[str, object]:
    root = _plugin_root()
    home = Path(os.environ.get("TESTAMUR_HOME") or Path.home() / ".testamur").expanduser()
    explicit_db = os.environ.get("TESTAMUR_DB")
    database = Path(explicit_db).expanduser() if explicit_db else home / "codex" / "evidence.db"

    testamur_spec = importlib.util.find_spec("testamur")
    project_gateway_spec = (
        importlib.util.find_spec("testamur.source_gateway_project_mcp")
        if testamur_spec is not None
        else None
    )
    mathhub_mcp_spec = importlib.util.find_spec("mathhub_mcp")
    command = shutil.which("testamur")
    gateway = shutil.which("testamur-gateway-mcp")
    mathhub_mcp_command = shutil.which("mathhub-mcp")

    required = {
        "plugin_manifest": root / ".codex-plugin" / "plugin.json",
        "hooks_manifest": root / "hooks" / "hooks.json",
        "mcp_manifest": root / ".mcp.json",
        "monitor_provider_manifest": root / "testamur-monitor-providers.json",
        "mcp_launcher": root / "mcp" / "serve.py",
        "mathhub_mcp_launcher": root / "mcp" / "mathhub.py",
    }
    files = {name: path.is_file() for name, path in required.items()}

    checks = {
        "testamur_python_import": testamur_spec is not None,
        "testamur_command": command is not None,
        "testamur_gateway_mcp_command": gateway is not None,
        "testamur_project_gateway_surface": project_gateway_spec is not None,
        "mathhub_mcp_surface": mathhub_mcp_spec is not None or mathhub_mcp_command is not None,
        "plugin_files": all(files.values()),
    }
    ready = all(checks.values())

    problems: list[dict[str, str]] = []
    if testamur_spec is None:
        problems.append({
            "code": "core_not_importable",
            "message": "The Testamur Python package is not importable in this environment.",
            "fix": "Install Testamur core in the same environment that launches Codex.",
        })
    if command is None:
        problems.append({
            "code": "testamur_not_on_path",
            "message": "The testamur CLI is not on PATH.",
            "fix": "Install Testamur core or activate the environment before starting Codex.",
        })
    if gateway is None:
        problems.append({
            "code": "gateway_not_on_path",
            "message": "testamur-gateway-mcp is not on PATH.",
            "fix": "Install Testamur core in the environment used to start Codex; then start a fresh Codex task.",
        })
    if testamur_spec is not None and project_gateway_spec is None:
        problems.append({
            "code": "project_gateway_surface_missing",
            "message": "Installed Testamur lacks the project-aware Source Gateway MCP surface.",
            "fix": "Upgrade Testamur core so source_gateway_project_mcp is available; the legacy gateway does not expose the existing-project supply-chain lifecycle.",
        })
    if mathhub_mcp_spec is None and mathhub_mcp_command is None:
        problems.append({
            "code": "mathhub_mcp_surface_missing",
            "message": "MathHub MCP is not importable and mathhub-mcp is not on PATH.",
            "fix": "Install the MathHub client package in the Codex environment or configure the plugin launcher with MATHHUB_ROOT.",
        })
    missing = [name for name, present in files.items() if not present]
    if missing:
        problems.append({
            "code": "plugin_package_incomplete",
            "message": "Required plugin files are missing: " + ", ".join(missing),
            "fix": "Reinstall the Testamur Codex plugin from the official repository/marketplace source.",
        })

    return {
        "ok": ready,
        "schema": "testamur.codex.doctor.v2",
        "ready_for_fresh_codex_session": ready,
        "checks": checks,
        "resolved": {
            "python": sys.executable,
            "testamur_command": command,
            "testamur_gateway_mcp_command": gateway,
            "mathhub_mcp_command": mathhub_mcp_command,
            "testamur_home": str(home),
            "testamur_db": str(database),
            "plugin_root": str(root),
        },
        "plugin_files": files,
        "problems": problems,
        "semantics": {
            "doctor_checks_installation_not_verification": True,
            "mcp_available_does_not_imply_source_verified": True,
            "mathhub_available_does_not_imply_claim_verified": True,
            "lean_remains_mathhub_verifier": True,
            "fetched_does_not_imply_relied": True,
        },
    }


def _render_human(report: dict[str, object]) -> str:
    checks = report["checks"]
    resolved = report["resolved"]
    lines = [
        "Testamur Codex doctor",
        "",
        f"[{'ok' if checks['testamur_python_import'] else '!!'}] Testamur Python import",
        f"[{'ok' if checks['testamur_command'] else '!!'}] testamur command",
        f"[{'ok' if checks['testamur_gateway_mcp_command'] else '!!'}] testamur-gateway-mcp command",
        f"[{'ok' if checks['testamur_project_gateway_surface'] else '!!'}] project-aware supply-chain MCP surface",
        f"[{'ok' if checks['mathhub_mcp_surface'] else '!!'}] MathHub MCP surface",
        f"[{'ok' if checks['plugin_files'] else '!!'}] plugin package files",
        "",
        f"Python: {resolved['python']}",
        f"TESTAMUR_HOME: {resolved['testamur_home']}",
        f"TESTAMUR_DB: {resolved['testamur_db']}",
    ]
    if report["ready_for_fresh_codex_session"]:
        lines += [
            "",
            "Ready: start a fresh Codex session from this environment.",
            "Project-aware Testamur supply-chain operations and the host-neutral MathHub MCP surface are available.",
        ]
    else:
        lines += ["", "Not ready for a fresh Codex session:"]
        for problem in report["problems"]:
            lines.append(f"- {problem['message']}")
            lines.append(f"  Fix: {problem['fix']}")
    lines += [
        "",
        "Boundary: installation available != source/claim verified; fetched != relied; Lean remains MathHub's verifier.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check whether Testamur core, project-aware MCP, MathHub MCP, and the Codex plugin are ready for a fresh Codex session.")
    parser.add_argument("--json", action="store_true", help="emit the machine-readable doctor report")
    args = parser.parse_args(argv)
    report = inspect_environment()
    if args.json:
        print(json.dumps(report, sort_keys=True, indent=2))
    else:
        print(_render_human(report))
    return 0 if report["ready_for_fresh_codex_session"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
