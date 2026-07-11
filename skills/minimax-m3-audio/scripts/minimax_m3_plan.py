#!/usr/bin/env python3
"""Call MiniMax-M3 through the OpenAI-compatible chat endpoint for coding plans."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://api.minimax.io/v1"
DEFAULT_MODEL = "MiniMax-M3"


def load_dotenv() -> None:
    for name in (".env.local", ".env"):
        path = Path.cwd() / name
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def post_json(url: str, api_key: str, payload: dict) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"MiniMax HTTP {exc.code}: {detail}") from exc


def extract_text(response: dict) -> str:
    choices = response.get("choices") or []
    if not choices:
        raise SystemExit(f"MiniMax response had no choices: {json.dumps(response)[:1000]}")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            elif isinstance(item, str):
                parts.append(item)
        content = "\n".join(part for part in parts if part)
    if not content:
        raise SystemExit(f"MiniMax response had no text content: {json.dumps(response)[:1000]}")
    return str(content).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Task or coding-plan request.")
    parser.add_argument("--out", help="Optional markdown output path.")
    parser.add_argument("--model", default=os.getenv("MINIMAX_MODEL", DEFAULT_MODEL))
    parser.add_argument("--base-url", default=os.getenv("MINIMAX_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--max-completion-tokens", type=int, default=2048)
    parser.add_argument(
        "--thinking",
        choices=("disabled", "adaptive"),
        default="disabled",
        help="MiniMax-M3 thinking mode. Default disables thinking for concise plan output.",
    )
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise SystemExit("MINIMAX_API_KEY is not set. Put it in the environment or ignored .env.local.")

    system = (
        "You are a senior coding planner. Return a practical implementation plan with "
        "assumptions, steps, risks, and verification. Do not include hidden reasoning."
    )
    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": args.prompt},
        ],
        "max_completion_tokens": args.max_completion_tokens,
        "temperature": args.temperature,
        "thinking": {"type": args.thinking},
    }

    url = args.base_url.rstrip("/") + "/chat/completions"
    response = post_json(url, api_key, payload)
    text = extract_text(response)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(out_path)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
