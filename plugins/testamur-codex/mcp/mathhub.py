from __future__ import annotations

import os
import sys
from pathlib import Path


def _candidate_roots() -> list[Path]:
    roots: list[Path] = []
    explicit = os.environ.get("MATHHUB_ROOT")
    if explicit:
        roots.append(Path(explicit).expanduser())
    plugin_root = Path(os.environ.get("PLUGIN_ROOT") or Path.cwd()).expanduser()
    roots.extend(
        [
            plugin_root.parent.parent / "Mathub",
            plugin_root.parent.parent.parent / "Mathub",
        ]
    )
    return roots


def _mcp_argv() -> list[str]:
    """Translate host-neutral MathHub environment configuration to MCP flags."""
    argv: list[str] = []
    base_url = os.environ.get("MATHHUB_URL")
    timeout = os.environ.get("MATHHUB_TIMEOUT")
    if base_url:
        argv.extend(["--base-url", base_url])
    if timeout:
        argv.extend(["--timeout", timeout])
    return argv


def main() -> int:
    try:
        from mathhub_mcp import main as mcp_main
    except ImportError:
        for root in _candidate_roots():
            if (root / "mathhub_mcp.py").is_file():
                sys.path.insert(0, str(root))
                break
        try:
            from mathhub_mcp import main as mcp_main
        except ImportError:
            print(
                "MathHub MCP could not import mathhub_mcp. Install the MathHub client surface "
                "or set MATHHUB_ROOT to a MathHub checkout containing mathhub_mcp.py.",
                file=sys.stderr,
            )
            return 1
    return int(mcp_main(_mcp_argv()))


if __name__ == "__main__":
    raise SystemExit(main())
