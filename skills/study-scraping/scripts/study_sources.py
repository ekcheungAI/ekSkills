#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCHEMA_VERSION = "research.v1"
TIKHUB_BASE_URL = os.environ.get("TIKHUB_API_BASE", "https://api.tikhub.io").rstrip("/")
OPENAPI_URL = f"{TIKHUB_BASE_URL}/openapi.json"
ALLOWED_PREFIXES = (
    "/api/v1/instagram/",
    "/api/v1/reddit/",
    "/api/v1/youtube/",
)
FORBIDDEN_PATH_TOKENS = ("cookie", "inbox", "login", "message", "private", "session")
MIN_REQUEST_INTERVAL = 0.1
DEFAULT_TIMEOUT = 45
MAX_RETRIES = 3
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILES = (
    Path.cwd() / ".env.local",
    SKILL_ROOT / ".env.local",
    Path.home() / ".codex" / ".env.local",
)
_last_request_at = 0.0


class SafetyError(RuntimeError):
    """The requested collection would cross a safety or access boundary."""


class ProviderError(RuntimeError):
    """TikHub returned a non-retryable provider error."""


def load_env(paths: tuple[Path, ...] = DEFAULT_ENV_FILES) -> None:
    values: dict[str, str] = {}
    for path in reversed(paths):
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    os.environ.update(values)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def environment_status() -> dict[str, dict[str, bool]]:
    return {"TIKHUB_API_KEY": {"available": bool(os.environ.get("TIKHUB_API_KEY"))}}


def require_api_key() -> str:
    value = os.environ.get("TIKHUB_API_KEY", "")
    if not value:
        raise ProviderError("TIKHUB_API_KEY is missing")
    return value


def parse_params(values: list[str]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid --param '{value}'; expected key=value")
        key, raw = value.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("Parameter name cannot be empty")
        normalized = raw.strip()
        if normalized.casefold() in {"true", "false"}:
            params[key] = normalized.casefold() == "true"
        elif re.fullmatch(r"-?\d+", normalized):
            params[key] = int(normalized)
        else:
            params[key] = normalized
    return params


def validate_endpoint(path: str) -> str:
    if not path.startswith("/"):
        path = f"/{path}"
    lowered = path.casefold()
    if not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise SafetyError(
            "Only public Instagram, YouTube, and Reddit TikHub routes are allowed"
        )
    if any(token in lowered for token in FORBIDDEN_PATH_TOKENS):
        raise SafetyError(
            "Login, cookie, private, session, inbox, and messaging routes are blocked"
        )
    return path


def validate_budgets(
    *, limit: int, page_budget: int, deep_fetch_limit: int
) -> dict[str, int]:
    if limit <= 0:
        raise ValueError("--limit must be greater than zero")
    if page_budget <= 0:
        raise ValueError("--page-budget must be greater than zero")
    if deep_fetch_limit < 0:
        raise ValueError("--deep-fetch-limit cannot be negative")
    return {
        "limit": limit,
        "page_budget": page_budget,
        "deep_fetch_limit": deep_fetch_limit,
    }


def _throttle(
    *,
    sleeper: Callable[[float], None],
    clock: Callable[[], float],
) -> None:
    global _last_request_at
    now = clock()
    remaining = MIN_REQUEST_INTERVAL - (now - _last_request_at)
    if _last_request_at and remaining > 0:
        sleeper(remaining)
        now = clock()
    _last_request_at = now


def request_json(
    path: str,
    params: dict[str, Any],
    *,
    api_key: str,
    timeout: int = DEFAULT_TIMEOUT,
    opener: Callable[..., Any] = urllib.request.urlopen,
    sleeper: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    path = validate_endpoint(path)
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{TIKHUB_BASE_URL}{path}"
    if query:
        url = f"{url}?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "study-scraping/2.0",
        },
    )

    for attempt in range(1, MAX_RETRIES + 1):
        _throttle(sleeper=sleeper, clock=clock)
        try:
            with opener(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
                payload = json.loads(raw) if raw else {}
                serialized = json.dumps(payload, ensure_ascii=False).casefold()
                if any(
                    marker in serialized
                    for marker in (
                        "login_required",
                        "login required",
                        "private account",
                    )
                ):
                    raise SafetyError("Source requires login or private access")
                return payload
        except urllib.error.HTTPError as exc:
            code = exc.code
            reason = exc.reason
            exc.close()
            if code in {401, 403, 429}:
                raise SafetyError(
                    f"TikHub/source access stopped after HTTP {code}; do not retry or bypass"
                ) from exc
            if code >= 500 and attempt < MAX_RETRIES:
                sleeper(2 ** (attempt - 1))
                continue
            raise ProviderError(f"TikHub HTTP {code}: {reason}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < MAX_RETRIES:
                sleeper(2 ** (attempt - 1))
                continue
            raise ProviderError(
                f"TikHub request failed after {MAX_RETRIES} attempts: {exc}"
            ) from exc
    raise ProviderError("TikHub request failed")


def fetch_openapi(
    *,
    opener: Callable[..., Any] = urllib.request.urlopen,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    request = urllib.request.Request(
        OPENAPI_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "study-scraping/2.0",
        },
    )
    with opener(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def endpoint_matches(pattern: str, spec: dict[str, Any]) -> list[dict[str, Any]]:
    needle = pattern.casefold()
    matches: list[dict[str, Any]] = []
    for path, methods in sorted(spec.get("paths", {}).items()):
        if needle not in path.casefold() or not any(
            path.startswith(prefix) for prefix in ALLOWED_PREFIXES
        ):
            continue
        operation = methods.get("get") or methods.get("post") or {}
        matches.append(
            {
                "path": path,
                "summary": operation.get("summary"),
                "parameters": [
                    {
                        "name": item.get("name"),
                        "required": bool(item.get("required")),
                    }
                    for item in operation.get("parameters", [])
                ],
            }
        )
    return matches


def _find_cursor(payload: Any, platform: str) -> tuple[str, Any] | None:
    keys = {
        "instagram": ("after", "next_cursor", "next_max_id"),
        "youtube": ("continuation_token", "continuation", "next_cursor"),
        "reddit": ("after", "next_cursor"),
    }.get(platform, ("next_cursor",))
    for item in _walk_dicts(payload):
        for key in keys:
            value = item.get(key)
            if value not in (None, ""):
                return key, value
    return None


def collect_pages(
    path: str,
    params: dict[str, Any],
    *,
    platform: str,
    page_budget: int,
    api_key: str,
    requester: Callable[..., dict[str, Any]] = request_json,
) -> list[dict[str, Any]]:
    if page_budget <= 0:
        raise ValueError("page_budget must be greater than zero")
    pages: list[dict[str, Any]] = []
    current_params = dict(params)
    for _ in range(page_budget):
        payload = requester(path, current_params, api_key=api_key)
        pages.append(payload)
        cursor = _find_cursor(payload, platform)
        if not cursor:
            break
        key, value = cursor
        current_params = dict(params)
        current_params[key] = value
    return pages


def command_params(command: str, **values: Any) -> dict[str, Any]:
    if command == "youtube-search":
        return {"search_query": values["query"]}
    if command == "youtube-video":
        return {"video_id": values["video_id"]}
    if command == "instagram-profile":
        return {"username": values["username"]}
    if command == "instagram-posts":
        return {"username": values["username"], "first": values.get("limit", 12)}
    if command == "reddit-search":
        return {
            "query": values["query"],
            "search_type": values.get("search_type", "post"),
            "sort": values.get("sort", "relevance"),
            "time_range": values.get("time_range", "month"),
            "safe_search": "strict",
            "allow_nsfw": 0,
        }
    raise ValueError(f"Unknown high-level command: {command}")


COMMANDS: dict[str, tuple[str, str, str]] = {
    "youtube-search": (
        "/api/v1/youtube/web_v2/get_general_search",
        "youtube",
        "search",
    ),
    "youtube-video": ("/api/v1/youtube/web_v2/get_video_info", "youtube", "video"),
    "instagram-profile": (
        "/api/v1/instagram/v3/get_user_profile",
        "instagram",
        "profile",
    ),
    "instagram-posts": ("/api/v1/instagram/v3/get_user_posts", "instagram", "posts"),
    "reddit-search": ("/api/v1/reddit/app/fetch_dynamic_search", "reddit", "search"),
}


def _walk_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from _walk_dicts(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_dicts(nested)


def _integer(value: Any) -> int:
    value = _text(value)
    if isinstance(value, str):
        value = value.replace(",", "")
        match = re.search(r"-?\d+", value)
        value = match.group(0) if match else 0
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _caption(value: Any) -> str:
    return _text(value)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        simple = value.get("simpleText") or value.get("text") or value.get("caption")
        if simple:
            return str(simple)
        runs = value.get("runs")
        if isinstance(runs, list):
            return "".join(
                str(run.get("text") or "") for run in runs if isinstance(run, dict)
            )
        return ""
    return str(value or "")


def _source_id(platform: str, url: str | None, title: str) -> str:
    return hashlib.sha256(
        f"tikhub|{platform}|{url or title}".encode("utf-8")
    ).hexdigest()[:16]


def _source_card(
    *,
    platform: str,
    url: str | None,
    title: str,
    author: str | None,
    published_at: str | None,
    metrics: dict[str, int],
    raw_ref: dict[str, Any],
    captured_at: str,
) -> dict[str, Any]:
    return {
        "source_id": _source_id(platform, url, title),
        "collector": "tikhub",
        "collectors": ["tikhub"],
        "platform": platform,
        "source_url": url,
        "title_or_text": title,
        "author": author,
        "published_at": published_at,
        "captured_at": captured_at,
        "metrics": metrics,
        "evidence_role": "signal",
        "claim_text": title,
        "claim_ids": [],
        "confidence": "low",
        "raw_ref": raw_ref,
    }


def normalize_tikhub(
    platform: str, operation: str, payload: dict[str, Any], *, limit: int
) -> list[dict[str, Any]]:
    serialized = json.dumps(payload, ensure_ascii=False).casefold()
    if any(
        marker in serialized
        for marker in ("login_required", "login required", "private account")
    ):
        raise SafetyError("Source requires login or private access")

    captured_at = utc_now()
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in _walk_dicts(payload):
        card: dict[str, Any] | None = None
        if platform == "youtube":
            video_id = item.get("videoId") or item.get("video_id")
            if operation == "video" and not video_id:
                video_id = item.get("id") if item.get("title") else None
            if video_id and (item.get("title") or item.get("video_title")):
                title = _text(item.get("title") or item.get("video_title"))
                card = _source_card(
                    platform="youtube",
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    title=title,
                    author=_text(
                        item.get("channelTitle")
                        or item.get("channel_name")
                        or item.get("shortBylineText")
                        or item.get("longBylineText")
                        or item.get("author")
                    )
                    or None,
                    published_at=_text(
                        item.get("publishedAt")
                        or item.get("published_at")
                        or item.get("publishedTimeText")
                    )
                    or None,
                    metrics={
                        "views": _integer(
                            item.get("viewCount")
                            or item.get("view_count")
                            or item.get("viewCountText")
                            or item.get("shortViewCountText")
                        ),
                        "likes": _integer(
                            item.get("likeCount") or item.get("like_count")
                        ),
                        "comments": _integer(
                            item.get("commentCount") or item.get("comment_count")
                        ),
                    },
                    raw_ref={"operation": operation, "video_id": str(video_id)},
                    captured_at=captured_at,
                )
        elif platform == "instagram" and operation == "profile":
            username = item.get("username")
            if username and any(
                key in item for key in ("biography", "follower_count", "full_name")
            ):
                title = str(item.get("full_name") or username)
                card = _source_card(
                    platform="instagram",
                    url=f"https://www.instagram.com/{username}/",
                    title=title,
                    author=str(username),
                    published_at=None,
                    metrics={"followers": _integer(item.get("follower_count"))},
                    raw_ref={"operation": operation, "user_id": item.get("id")},
                    captured_at=captured_at,
                )
                card["profile_summary"] = item.get("biography")
        elif platform == "instagram" and operation == "posts":
            code = item.get("code") or item.get("shortcode")
            if code:
                caption = _caption(item.get("caption")) or f"Instagram post {code}"
                card = _source_card(
                    platform="instagram",
                    url=f"https://www.instagram.com/p/{code}/",
                    title=caption,
                    author=item.get("username") or item.get("owner_username"),
                    published_at=item.get("taken_at") or item.get("published_at"),
                    metrics={
                        "likes": _integer(item.get("like_count")),
                        "comments": _integer(item.get("comment_count")),
                        "plays": _integer(
                            item.get("play_count") or item.get("video_view_count")
                        ),
                    },
                    raw_ref={"operation": operation, "code": str(code)},
                    captured_at=captured_at,
                )
        elif platform == "reddit":
            identifier = item.get("id")
            title = item.get("title")
            if identifier and title:
                permalink = item.get("permalink") or f"/comments/{identifier}/"
                url = str(permalink)
                if url.startswith("/"):
                    url = f"https://www.reddit.com{url}"
                card = _source_card(
                    platform="reddit",
                    url=url,
                    title=str(title),
                    author=item.get("author") or item.get("subreddit"),
                    published_at=item.get("created_utc") or item.get("created_at"),
                    metrics={
                        "score": _integer(item.get("score")),
                        "comments": _integer(item.get("num_comments")),
                    },
                    raw_ref={"operation": operation, "post_id": str(identifier)},
                    captured_at=captured_at,
                )

        if card is None:
            identifier = item.get("id") or item.get("comment_id") or item.get("cid")
            text = item.get("text") or item.get("content") or item.get("title")
            if identifier and text:
                url = item.get("url") or item.get("permalink")
                if (
                    isinstance(url, str)
                    and url.startswith("/")
                    and platform == "reddit"
                ):
                    url = f"https://www.reddit.com{url}"
                card = _source_card(
                    platform=platform,
                    url=str(url) if url else None,
                    title=str(text),
                    author=item.get("author")
                    or item.get("username")
                    or item.get("channelTitle"),
                    published_at=item.get("published_at")
                    or item.get("created_at")
                    or item.get("created_utc"),
                    metrics={
                        "likes": _integer(
                            item.get("like_count") or item.get("likeCount")
                        ),
                        "replies": _integer(
                            item.get("reply_count") or item.get("replyCount")
                        ),
                    },
                    raw_ref={"operation": operation, "item_id": str(identifier)},
                    captured_at=captured_at,
                )

        if card and card["source_id"] not in seen:
            seen.add(card["source_id"])
            cards.append(card)
            if len(cards) >= limit:
                break
    return cards


def build_packet(
    question: str,
    platform: str,
    operation: str,
    payload: dict[str, Any],
    *,
    limit: int,
    page_budget: int = 1,
    deep_fetch_limit: int = 0,
) -> dict[str, Any]:
    budget = validate_budgets(
        limit=limit,
        page_budget=page_budget,
        deep_fetch_limit=deep_fetch_limit,
    )
    cards = normalize_tikhub(platform, operation, payload, limit=limit)
    pages_fetched = (
        len(payload.get("pages", [])) if isinstance(payload.get("pages"), list) else 1
    )
    missing = [] if cards else ["no_normalized_source_cards"]
    return {
        "schema_version": SCHEMA_VERSION,
        "research_question": question,
        "mode": "standard",
        "captured_at": utc_now(),
        "coverage": {
            "checked": ["tikhub"],
            "missing": missing,
            "provider_errors": [],
            "budget": budget,
            "pages_fetched": pages_fetched,
        },
        "source_cards": cards,
        "claims": [],
        "contradictions": [],
        "audience_angles": [],
        "route": "research_more",
    }


def add_budget_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--page-budget", type=int, default=1)
    parser.add_argument("--deep-fetch-limit", type=int, default=0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect public TikHub evidence into research.v1 source cards."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "check-env", help="Show boolean TikHub credential availability."
    )

    endpoints = subparsers.add_parser(
        "tikhub-endpoints", help="Inspect current public TikHub routes."
    )
    endpoints.add_argument("pattern")

    generic = subparsers.add_parser(
        "tikhub-get", help="Call an allowed public TikHub GET route."
    )
    generic.add_argument("path")
    generic.add_argument("--param", action="append", default=[])
    generic.add_argument(
        "--platform", choices=("youtube", "instagram", "reddit"), required=True
    )
    generic.add_argument("--operation", default="search")
    generic.add_argument("--question", default="TikHub public-source collection")
    add_budget_args(generic)

    youtube_search = subparsers.add_parser(
        "youtube-search", help="Search public YouTube content through TikHub."
    )
    youtube_search.add_argument("query")
    add_budget_args(youtube_search)

    youtube_video = subparsers.add_parser(
        "youtube-video", help="Fetch public YouTube video details through TikHub."
    )
    youtube_video.add_argument("video_id")
    add_budget_args(youtube_video)

    instagram_profile = subparsers.add_parser(
        "instagram-profile", help="Fetch a public Instagram profile through TikHub."
    )
    instagram_profile.add_argument("username")
    add_budget_args(instagram_profile)

    instagram_posts = subparsers.add_parser(
        "instagram-posts", help="Fetch public Instagram posts through TikHub."
    )
    instagram_posts.add_argument("username")
    add_budget_args(instagram_posts)

    reddit_search = subparsers.add_parser(
        "reddit-search", help="Search public Reddit posts through TikHub."
    )
    reddit_search.add_argument("query")
    reddit_search.add_argument("--search-type", default="post")
    reddit_search.add_argument("--sort", default="relevance")
    reddit_search.add_argument("--time-range", default="month")
    add_budget_args(reddit_search)
    return parser


def execute(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "check-env":
        return {"env": environment_status()}
    if args.command == "tikhub-endpoints":
        return {
            "openapi": OPENAPI_URL,
            "matches": endpoint_matches(args.pattern, fetch_openapi()),
        }

    budget = validate_budgets(
        limit=args.limit,
        page_budget=args.page_budget,
        deep_fetch_limit=args.deep_fetch_limit,
    )
    if args.command == "tikhub-get":
        path = validate_endpoint(args.path)
        params = parse_params(args.param)
        platform = args.platform
        operation = args.operation
        question = args.question
    else:
        path, platform, operation = COMMANDS[args.command]
        command_values = {
            key: value for key, value in vars(args).items() if key != "command"
        }
        params = command_params(args.command, **command_values)
        question = (
            getattr(args, "query", None)
            or getattr(args, "username", None)
            or getattr(args, "video_id", None)
        )
        question = f"TikHub {args.command}: {question}"

    pages = collect_pages(
        path,
        params,
        platform=platform,
        page_budget=budget["page_budget"],
        api_key=require_api_key(),
    )
    payload = {"pages": pages}
    return build_packet(
        question,
        platform,
        operation,
        payload,
        limit=budget["limit"],
        page_budget=budget["page_budget"],
        deep_fetch_limit=budget["deep_fetch_limit"],
    )


def main() -> int:
    load_env()
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = execute(args)
    except (ProviderError, SafetyError, ValueError) as exc:
        print(
            json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
