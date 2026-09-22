from __future__ import annotations

import importlib.util
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "testamur-codex"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_bootstrap(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_codex_plugin_manifest_points_to_bundled_hooks_and_legacy_mcp() -> None:
    manifest = _json(PLUGIN / ".codex-plugin" / "plugin.json")
    assert manifest["name"] == "testamur-codex"
    assert manifest["version"] == "1.1.0"
    assert manifest["hooks"] == "./hooks/hooks.json"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert (PLUGIN / "hooks" / "hooks.json").is_file()
    assert (PLUGIN / "hooks" / "capture.py").is_file()
    assert (PLUGIN / ".mcp.json").is_file()
    assert not (PLUGIN / "mcp.json").exists()
    assert (PLUGIN / "mcp" / "serve.py").is_file()


def test_codex_hooks_cover_session_and_tool_lifecycle_synchronously() -> None:
    config = _json(PLUGIN / "hooks" / "hooks.json")
    hooks = config["hooks"]
    assert set(hooks) == {"SessionStart", "PostToolUse", "SessionEnd"}
    assert hooks["SessionStart"][0]["matcher"] == "*"
    assert hooks["PostToolUse"][0]["matcher"] == "*"

    for groups in hooks.values():
        for group in groups:
            for handler in group["hooks"]:
                assert handler["type"] == "command"
                assert "${PLUGIN_ROOT}/hooks/capture.py" in handler["command"]
                assert handler.get("async") is not True


def test_legacy_mcp_config_uses_plugin_root_cwd_and_callable_server_key() -> None:
    config = _json(PLUGIN / ".mcp.json")
    assert "$schema" not in config
    names = list(config["mcpServers"])
    assert names == ["testamur_source_gateway"]
    # Codex has had callable-tool exposure bugs with hyphenated plugin MCP keys.
    assert re.fullmatch(r"[A-Za-z0-9_]+", names[0])
    server = config["mcpServers"][names[0]]
    assert server["command"] == "python3"
    assert server["args"] == ["mcp/serve.py"]
    assert server["cwd"] == "."
    assert "env" not in server


def test_repo_marketplace_discovers_testamur_codex_plugin() -> None:
    marketplace = _json(ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    entry = entries["testamur-codex"]
    assert entry["source"] == {
        "source": "local",
        "path": "./plugins/testamur-codex",
    }


def test_plugin_bootstraps_do_not_vendor_core() -> None:
    hook_bootstrap = (PLUGIN / "hooks" / "capture.py").read_text(encoding="utf-8")
    mcp_bootstrap = (PLUGIN / "mcp" / "serve.py").read_text(encoding="utf-8")
    for bootstrap in (hook_bootstrap, mcp_bootstrap):
        assert "TESTAMUR_DB" in bootstrap
        assert "TESTAMUR_HOME" in bootstrap
        assert "subprocess" not in bootstrap
    assert "from testamur.codex_gateway_hook import main" in hook_bootstrap
    assert "from testamur.repository_binding_mcp import main" in mcp_bootstrap
    assert "from testamur.source_gateway_project_mcp import main" in mcp_bootstrap
    assert "from testamur.source_gateway_mcp import main" in mcp_bootstrap


def test_plugin_readme_exposes_project_supply_chain_semantics() -> None:
    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    for tool in (
        "testamur.project_repository_binding",
        "testamur.set_project_repository_binding_enabled",
        "testamur.project_repository_unbind",
        "testamur.project_scan",
        "testamur.project_supply_chain",
        "testamur.project_supply_chain_diff",
        "testamur.project_advisory_revalidation",
    ):
        assert tool in readme
    assert "EXPOSED_TO_MODEL != RELIED" in readme
    assert "changed != invalid" in readme
    assert "No generic trust score" in readme
    assert "testamur.repository_binding_mcp" in readme


def test_plugin_bootstraps_resolve_same_testamur_owned_database(monkeypatch, tmp_path: Path) -> None:
    hook = _load_bootstrap(PLUGIN / "hooks" / "capture.py", "testamur_plugin_hook_bootstrap")
    mcp = _load_bootstrap(PLUGIN / "mcp" / "serve.py", "testamur_plugin_mcp_bootstrap")
    state_root = tmp_path / "testamur-home"
    expected = state_root / "codex" / "evidence.db"

    for bootstrap in (hook, mcp):
        monkeypatch.setenv("TESTAMUR_HOME", str(state_root))
        # Hooks receive PLUGIN_DATA while legacy plugin MCP servers do not. The
        # state path must therefore remain independent of this host asymmetry.
        monkeypatch.setenv("PLUGIN_DATA", str(tmp_path / "host-only-plugin-data"))
        monkeypatch.delenv("TESTAMUR_DB", raising=False)
        resolved = bootstrap._configure_testamur_state()
        assert resolved == expected
        assert Path(os.environ["TESTAMUR_DB"]) == expected


def test_plugin_bootstraps_register_monitor_provider_manifest(monkeypatch, tmp_path: Path) -> None:
    hook = _load_bootstrap(PLUGIN / "hooks" / "capture.py", "testamur_plugin_hook_provider")
    mcp = _load_bootstrap(PLUGIN / "mcp" / "serve.py", "testamur_plugin_mcp_provider")
    home = tmp_path / "testamur-home"
    expected = home / "providers" / "testamur-codex.json"
    source = _json(PLUGIN / "testamur-monitor-providers.json")

    for bootstrap in (hook, mcp):
        monkeypatch.setenv("TESTAMUR_HOME", str(home))
        monkeypatch.setenv("PLUGIN_ROOT", str(PLUGIN))
        registered = bootstrap._register_monitor_provider_manifest()
        assert registered == expected
        assert _json(expected) == source

    assert source["schema"] == "testamur.monitor-providers.v1"
    providers = {provider["name"]: provider for provider in source["providers"]}
    assert "github_branch" in providers
    assert providers["github_branch"]["locator_template"].startswith(
        "https://github.com/"
    )


def test_plugin_bootstraps_preserve_explicit_database_override(monkeypatch, tmp_path: Path) -> None:
    hook = _load_bootstrap(PLUGIN / "hooks" / "capture.py", "testamur_plugin_hook_override")
    mcp = _load_bootstrap(PLUGIN / "mcp" / "serve.py", "testamur_plugin_mcp_override")
    explicit = tmp_path / "explicit.db"

    for bootstrap in (hook, mcp):
        monkeypatch.setenv("TESTAMUR_HOME", str(tmp_path / "ignored-home"))
        monkeypatch.setenv("TESTAMUR_DB", str(explicit))
        resolved = bootstrap._configure_testamur_state()
        assert resolved == explicit
        assert Path(os.environ["TESTAMUR_DB"]) == explicit


def test_doctor_script_is_packaged() -> None:
    doctor = ROOT / "plugins" / "testamur-codex" / "scripts" / "doctor.py"
    text = doctor.read_text(encoding="utf-8")
    assert doctor.is_file()
    assert "testamur.codex.doctor.v3" in text
    assert "ready_for_fresh_codex_session" in text
    assert "testamur-gateway-mcp" in text
    assert "testamur.repository_binding_mcp" in text
    assert "testamur_repository_binding_mcp_surface" in text
    assert "fetched_does_not_imply_relied" in text
