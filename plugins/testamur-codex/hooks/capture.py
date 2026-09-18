from __future__ import annotations

import os
import sys
from pathlib import Path


def _repo_root() -> Path | None:
    # Development/local-marketplace fallback. Installed marketplace copies should
    # normally resolve the packaged console entry point or importable package.
    plugin_root = Path(os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    candidate = plugin_root.parent.parent
    if (candidate / "testamur" / "codex_gateway_hook.py").is_file():
        return candidate
    return None


def _configure_testamur_state() -> Path:
    """Choose the stable Codex integration database shared with the MCP launcher.

    Legacy Codex plugin hooks receive PLUGIN_DATA, but legacy plugin MCP servers
    currently do not receive the same plugin-data signal. Using PLUGIN_DATA here
    would therefore split lifecycle capture from exact source capture. Until the
    MCP runtime exposes a common writable plugin-data root, Testamur owns a stable
    per-user Codex store instead.
    """

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
        from testamur.codex_gateway_hook import main as hook_main
    except ImportError:
        root = _repo_root()
        if root is not None:
            sys.path.insert(0, str(root))
        try:
            from testamur.codex_gateway_hook import main as hook_main
        except ImportError:
            print(
                "Testamur Codex hook could not import the Testamur core package. "
                "Install Testamur in this environment (for development: python -m pip install -e .).",
                file=sys.stderr,
            )
            return 1
    return int(hook_main())


if __name__ == "__main__":
    raise SystemExit(main())
