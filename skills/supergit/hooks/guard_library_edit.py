#!/usr/bin/env python3
"""Claude Code PreToolUse hook: refuse Edit/Write/MultiEdit inside a guarded library.

The library (a project's shared main checkout) is read-only by rule; rules get
forgotten mid-session, hooks do not. Reads the hook payload on stdin, exits 2
with a message when the target path is inside a guarded library and not inside
a room (`.claude/worktrees/…` or `.worktrees/…`).

Guarded libraries come from ../config.json → "guarded_libraries". Set
SUPERGIT_GUARD_ALL=1 to guard every project listed in config.json instead.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ROOM_MARKERS = ("/.claude/worktrees/", "/.worktrees/")


def guarded_paths() -> list[Path]:
    paths: list[str] = []
    cfg = SKILL_DIR / "config.json"
    if cfg.exists():
        paths = json.loads(cfg.read_text()).get("guarded_libraries", [])
    if os.environ.get("SUPERGIT_GUARD_ALL") == "1" and cfg.exists():
        paths += [p["path"] for p in json.loads(cfg.read_text()).get("projects", []) if isinstance(p, dict) and p.get("path")]
    return [Path(os.path.expanduser(p)).resolve() for p in paths]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("tool_name") not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        return 0
    target = (payload.get("tool_input") or {}).get("file_path") or (payload.get("tool_input") or {}).get("notebook_path")
    if not target:
        return 0
    path = Path(target).resolve()
    if any(m in str(path) + "/" for m in ROOM_MARKERS):
        return 0
    for lib in guarded_paths():
        try:
            path.relative_to(lib)
        except ValueError:
            continue
        print(f"supergit: `{lib.name}` is a library (read-only main checkout). "
              f"Work in a room instead: `supergit start <slug>` — then edit under {lib}/.claude/worktrees/…",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
