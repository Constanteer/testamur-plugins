from __future__ import annotations

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
