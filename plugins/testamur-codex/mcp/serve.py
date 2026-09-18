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
    if (candidate / "testamur" / "source_gateway_mcp.py").is_file():
        return candidate
    return None


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


def main() -> int:
    _configure_testamur_state()
    try:
        from testamur.source_gateway_mcp import main as mcp_main
    except ImportError:
        root = _repo_root()
        if root is not None:
            sys.path.insert(0, str(root))
        try:
            from testamur.source_gateway_mcp import main as mcp_main
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
