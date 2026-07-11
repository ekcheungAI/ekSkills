#!/usr/bin/env python3
"""Read-only checks and dry-run scheduling helper for social-media-scheduler."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from typing import Iterable
from urllib import parse, request


THREADS_BASE = "https://graph.threads.net/v1.0"
UPLOAD_POST_BASE = "https://api.upload-post.com/api"


def _json_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
) -> tuple[int, dict]:
    req = request.Request(url, method=method, headers=headers or {}, data=data)
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except Exception as exc:  # pragma: no cover - diagnostic CLI helper
        print(f"Request failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _multipart(fields: dict[str, str], repeated: dict[str, Iterable[str]]) -> tuple[bytes, str]:
    boundary = f"codex-{uuid.uuid4().hex}"
    parts: list[bytes] = []

    def add_field(name: str, value: str) -> None:
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        parts.append(str(value).encode())
        parts.append(b"\r\n")

    for name, value in fields.items():
        add_field(name, value)

    for name, values in repeated.items():
        for value in values:
            add_field(name, value)

    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), boundary


def check_threads(_: argparse.Namespace) -> None:
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Missing THREADS_ACCESS_TOKEN")

    profile_url = (
        f"{THREADS_BASE}/me?"
        + parse.urlencode({"fields": "id,username", "access_token": token})
    )
    status, profile = _json_request(profile_url)

    limit_url = f"{THREADS_BASE}/me/threads_publishing_limit?" + parse.urlencode(
        {"access_token": token}
    )
    limit_status, limit = _json_request(limit_url)

    print(
        json.dumps(
            {
                "profile_status": status,
                "username": profile.get("username"),
                "has_id": bool(profile.get("id")),
                "publishing_limit_status": limit_status,
                "publishing_limit": limit,
            },
            indent=2,
        )
    )


def check_upload_post(_: argparse.Namespace) -> None:
    api_key = os.environ.get("UPLOAD_POST_API_KEY")
    if not api_key:
        raise SystemExit("Missing UPLOAD_POST_API_KEY")

    status, payload = _json_request(
        f"{UPLOAD_POST_BASE}/uploadposts/me",
        headers={"Authorization": f"Apikey {api_key}"},
    )
    print(json.dumps({"status": status, "response": payload}, indent=2))


def schedule_upload_text(args: argparse.Namespace) -> None:
    fields = {
        "user": args.user,
        "title": args.text,
        "timezone": args.timezone,
    }
    if args.scheduled_date:
        fields["scheduled_date"] = args.scheduled_date
    if args.first_comment:
        fields["first_comment"] = args.first_comment

    repeated = {"platform[]": args.platform}

    preview = {
        "endpoint": f"{UPLOAD_POST_BASE}/upload_text",
        "fields": fields,
        "platforms": args.platform,
        "dry_run": not args.execute,
    }
    print(json.dumps(preview, indent=2))

    if not args.execute:
        return

    api_key = os.environ.get("UPLOAD_POST_API_KEY")
    if not api_key:
        raise SystemExit("Missing UPLOAD_POST_API_KEY")

    body, boundary = _multipart(fields, repeated)
    status, payload = _json_request(
        f"{UPLOAD_POST_BASE}/upload_text",
        method="POST",
        headers={
            "Authorization": f"Apikey {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Idempotency-Key": args.idempotency_key or uuid.uuid4().hex,
        },
        data=body,
    )
    print(json.dumps({"status": status, "response": payload}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    check_threads_cmd = sub.add_parser("check-threads")
    check_threads_cmd.set_defaults(func=check_threads)

    check_upload_post_cmd = sub.add_parser("check-upload-post")
    check_upload_post_cmd.set_defaults(func=check_upload_post)

    schedule_cmd = sub.add_parser("schedule-upload-text")
    schedule_cmd.add_argument("--user", required=True)
    schedule_cmd.add_argument("--platform", action="append", required=True)
    schedule_cmd.add_argument("--text", required=True)
    schedule_cmd.add_argument("--scheduled-date")
    schedule_cmd.add_argument("--timezone", default="Asia/Hong_Kong")
    schedule_cmd.add_argument("--first-comment")
    schedule_cmd.add_argument("--idempotency-key")
    schedule_cmd.add_argument("--execute", action="store_true")
    schedule_cmd.set_defaults(func=schedule_upload_text)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
