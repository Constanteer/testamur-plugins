from __future__ import annotations

import importlib.util
import json
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def test_plugin_declares_separate_mathhub_mcp_server() -> None:
    manifest = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
    servers = manifest["mcpServers"]
    assert servers["testamur_source_gateway"]["args"] == ["mcp/serve.py"]
    assert servers["mathhub"]["args"] == ["mcp/mathhub.py"]
    assert servers["mathhub"]["cwd"] == "."


def test_mathhub_launcher_keeps_mathhub_as_separate_surface() -> None:
    source = (PLUGIN_ROOT / "mcp" / "mathhub.py").read_text(encoding="utf-8")
    assert "from mathhub_mcp import main as mcp_main" in source
    assert "MATHHUB_ROOT" in source
    assert "source_gateway_mcp" not in source


def test_mathhub_launcher_forwards_host_neutral_endpoint_environment(monkeypatch) -> None:
    path = PLUGIN_ROOT / "mcp" / "mathhub.py"
    spec = importlib.util.spec_from_file_location("testamur_plugin_mathhub_launcher", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    monkeypatch.setenv("MATHHUB_URL", "https://mathhub.example/api")
    monkeypatch.setenv("MATHHUB_TIMEOUT", "45")
    assert module._mcp_argv() == [
        "--base-url",
        "https://mathhub.example/api",
        "--timeout",
        "45",
    ]

    monkeypatch.delenv("MATHHUB_URL")
    monkeypatch.delenv("MATHHUB_TIMEOUT")
    assert module._mcp_argv() == []
