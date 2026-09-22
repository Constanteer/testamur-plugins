from __future__ import annotations

import os
import sys
from pathlib import Path


def _repo_root() -> Path | None:
    # This launcher normally starts with cwd=PLUGIN_ROOT from the legacy Codex
    # .mcp.json declaration. The explicit environment path remains preferable
    # when Codex provides it.
    plugin_root = Path(os.environ.get("PLUGIN_ROOT") or Path.cwd())
    candidate = plugin_root.parent.parent
    if (candidate / "testamur" / "repository_binding_mcp.py").is_file():
        return candidate
    if (candidate / "testamur" / "source_gateway_project_mcp.py").is_file():
        return candidate
    if (candidate / "testamur" / "source_gateway_mcp.py").is_file():
        return candidate
    return None


def _plugin_root() -> Path:
    explicit = os.environ.get("PLUGIN_ROOT")
    if explicit:
        return Path(explicit).expanduser()
    return Path(__file__).resolve().parents[1]


def _register_monitor_provider_manifest() -> Path | None:
    source = _plugin_root() / "testamur-monitor-providers.json"
    if not source.is_file():
        return None
    home = os.environ.get("TESTAMUR_HOME")
    root = Path(home).expanduser() if home else Path.home() / ".testamur"
    target = root / "providers" / "testamur-codex.json"
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = source.read_bytes()
        if not target.exists() or target.read_bytes() != payload:
            target.write_bytes(payload)
    except OSError:
        return None
    return target


def _configure_testamur_state() -> Path:
    """Choose the same stable database as the lifecycle hook bootstrap."""

    explicit = os.environ.get("TESTAMUR_DB")
    if explicit:
        database = Path(explicit).expanduser()
    else:
        home = os.environ.get("TESTAMUR_HOME")
        root = Path(home).expanduser() if home else Path.home() / ".testamur"
        database = root / "codex" / "evidence.db"
        os.environ["TESTAMUR_DB"] = str(database)
    return database


def _import_mcp_main():
    try:
        # Match the installed core's public testamur-gateway-mcp entrypoint.
        # This layer installs repository-binding lifecycle tools as well as the
        # complete Project supply-chain/advisory extension.
        from testamur.repository_binding_mcp import main as mcp_main
        return mcp_main
    except ImportError:
        try:
            from testamur.source_gateway_project_mcp import main as mcp_main
            return mcp_main
        except ImportError:
            # Compatibility with older installed Testamur remains deliberate:
            # source capture still works, while Project/binding lifecycle tools
            # become available as soon as the core package is upgraded.
            from testamur.source_gateway_mcp import main as mcp_main
            return mcp_main


def main() -> int:
    _configure_testamur_state()
    _register_monitor_provider_manifest()
    try:
        mcp_main = _import_mcp_main()
    except ImportError:
        root = _repo_root()
        if root is not None:
            sys.path.insert(0, str(root))
        try:
            mcp_main = _import_mcp_main()
        except ImportError:
            print(
                "Testamur Source Gateway MCP could not import the Testamur core package. "
                "Install Testamur in this environment (for development: python -m pip install -e .).",
                file=sys.stderr,
            )
            return 1
    return int(mcp_main())


if __name__ == "__main__":
    raise SystemExit(main())
