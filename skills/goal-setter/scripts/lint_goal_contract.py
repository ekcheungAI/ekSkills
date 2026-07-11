#!/usr/bin/env python3
"""Validate goal-setter goal contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_MARKERS = [
    ("command", [r"^\s*/goal\b"]),
    ("verification", [r"^Verification[:：]", r"^驗證[:：]"]),
    ("constraints", [r"^Constraints[:：]", r"^約束[:：]"]),
    ("boundaries", [r"^Boundaries[:：]", r"^邊界[:：]"]),
    ("iteration policy", [r"^Iteration policy[:：]", r"^迭代策略[:：]"]),
    ("stop when", [r"^Stop when[:：]", r"^完成條件[:：]", r"^停止條件[:：]"]),
    ("pause if", [r"^Pause if[:：]", r"^暫停條件[:：]", r"^阻塞條件[:：]"]),
]

PLACEHOLDERS = [
    r"\[[^\]]+\]",
    r"<[^>]+>",
    r"\bTODO\b",
    r"\bTBD\b",
    r"待補",
    r"待定",
]

VAGUE_DANGER = [
    r"make sure it works",
    r"edit anything",
    r"change whatever",
    r"keep trying",
    r"until it (looks|seems|feels) good",
    r"隨便改",
    r"一直試",
    r"直到滿意",
    r"感覺可以",
]

EVIDENCE_WORDS = [
    r"\b(run|start|open|test|build|lint|typecheck|verify|inspect|capture|screenshot|log|artifact|file|url|api|browser|local)\b",
    r"(運行|執行|啟動|打開|測試|構建|檢查|驗證|讀取|截圖|日誌|產物|文件|連結|接口|瀏覽器|本地|證據)",
]


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def marker_line(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(rf"{pattern}\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def lint_text(text: str, source: str) -> list[str]:
    errors: list[str] = []

    for name, patterns in REQUIRED_MARKERS:
        if not has_any(text, patterns):
            errors.append(f"{source}: missing {name}")

    if re.search(r"^\s*/目標\b|^\s*/目标\b", text, flags=re.MULTILINE):
        errors.append(f"{source}: use `/goal` as the command prefix")

    for pattern in PLACEHOLDERS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{source}: unresolved placeholder matched {pattern!r}")

    for pattern in VAGUE_DANGER:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{source}: vague dangerous instruction matched {pattern!r}")

    goal_line = next((line.strip() for line in text.splitlines() if line.strip().startswith("/goal")), "")
    if goal_line and len(goal_line.removeprefix("/goal").strip()) < 24:
        errors.append(f"{source}: goal outcome is too short")

    verification = marker_line(text, REQUIRED_MARKERS[1][1])
    if verification and not has_any(verification, EVIDENCE_WORDS):
        errors.append(f"{source}: verification should name concrete evidence")

    for name, patterns in REQUIRED_MARKERS[1:]:
        content = marker_line(text, patterns)
        if content and len(content) < 16:
            errors.append(f"{source}: {name} content is too thin")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: lint_goal_contract.py <file> [<file> ...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for raw in argv[1:]:
        path = Path(raw)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: cannot read file: {exc}")
            continue
        errors.extend(lint_text(text, str(path)))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Goal contract lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
