#!/usr/bin/env python3
"""Generate Claude Code / Codex wrappers for the agent roster, or check they are current.

  build_agent_roster.py            write claude/<slug>.md and codex/<slug>.toml
  build_agent_roster.py --check    exit 1 if any wrapper differs from what would be generated

Run from anywhere; paths are resolved relative to this skill folder (the parent of scripts/).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_DIR = SKILL_ROOT / "claude"
CODEX_DIR = SKILL_ROOT / "codex"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

BOUNDARY = (
    "You are an extra helping role, not a worker with new powers. The calling agent owns "
    "the brief, file ownership, integration, verification and delivery. You never call "
    "ship/merge/finish/abandon, never publish, never contact anyone, never widen "
    "permissions. Return findings and deliverables in the shape your profile lists, with "
    "evidence."
)


def load_roster() -> dict:
    data = json.loads((SKILL_ROOT / "roster.json").read_text())
    seen = set()
    for role in data["roles"]:
        slug = role["slug"]
        if not SLUG_RE.match(slug):
            raise SystemExit(f"slug must be lowercase-hyphen: {slug}")
        if slug in seen:
            raise SystemExit(f"duplicate slug: {slug}")
        seen.add(slug)
        if not (SKILL_ROOT / slug / "profile.md").is_file():
            raise SystemExit(f"missing profile: {slug}/profile.md")
        if "\n" in role["description"] or len(role["description"]) > 400:
            raise SystemExit(f"description must be one line <= 400 chars: {slug}")
    return data


def claude_wrapper(role: dict) -> str:
    slug = role["slug"]
    return (
        "---\n"
        f"name: {slug}\n"
        f"description: {role['description']}\n"
        "model: inherit\n"
        "---\n"
        f"Read `{slug}/profile.md` in this skill folder first and act as that role.\n\n"
        f"{BOUNDARY}\n"
    )


def codex_wrapper(role: dict) -> str:
    slug = role["slug"]
    name = slug.replace("-", "_")
    desc = role["description"].replace("\\", "\\\\").replace('"', '\\"')
    body = (
        f"Read {slug}/profile.md in this skill folder first and act as that role.\n\n"
        f"{BOUNDARY}\n"
    )
    return (
        f'name = "{name}"\n'
        f'description = "{desc}"\n\n'
        'developer_instructions = """\n'
        f"{body}"
        '"""\n'
    )


def expected_files(data: dict) -> dict[Path, str]:
    out: dict[Path, str] = {}
    for role in data["roles"]:
        out[CLAUDE_DIR / f"{role['slug']}.md"] = claude_wrapper(role)
        out[CODEX_DIR / f"{role['slug']}.toml"] = codex_wrapper(role)
    return out


def write(files: dict[Path, str]) -> None:
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print(f"wrote {len(files)} wrapper files")


def check(files: dict[Path, str]) -> int:
    bad = [p for p, c in files.items() if not p.is_file() or p.read_text() != c]
    for p in bad:
        print(f"stale or missing: {p.relative_to(SKILL_ROOT)}")
    if bad:
        print("run scripts/build_agent_roster.py to regenerate")
        return 1
    print(f"{len(files)} wrapper files current")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    data = load_roster()
    files = expected_files(data)
    if args.check:
        return check(files)
    write(files)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
