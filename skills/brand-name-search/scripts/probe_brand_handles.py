#!/usr/bin/env python3
"""First-pass brand domain and social handle probe.

This script intentionally reports screening signals, not final availability.
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Iterable


PLATFORMS = {
    "instagram": "https://www.instagram.com/{handle}/",
    "tiktok": "https://www.tiktok.com/@{handle}",
    "x": "https://x.com/{handle}",
    "threads": "https://www.threads.net/@{handle}",
    "youtube": "https://www.youtube.com/@{handle}",
    "pinterest": "https://www.pinterest.com/{handle}/",
    "facebook": "https://www.facebook.com/{handle}",
    "github": "https://github.com/{handle}",
    "etsy": "https://www.etsy.com/shop/{handle}",
    "shopify": "https://{handle}.myshopify.com",
}

SUFFIXES = ("", "hq", "co", "studio", "club", "world", "shop", "official")


@dataclass
class ProbeResult:
    target: str
    kind: str
    signal: str
    detail: str


def slugify_domain(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def slugify_handle(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def candidate_handles(name: str, limit: int) -> list[str]:
    base = slugify_handle(name)
    if not base:
        return []
    handles = []
    for suffix in SUFFIXES:
        handle = f"{base}{suffix}"
        if handle not in handles:
            handles.append(handle)
        if len(handles) >= limit:
            break
    return handles


def check_http(url: str, timeout: float) -> tuple[str, str]:
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": "Mozilla/5.0 brand-name-search screening probe",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        status = exc.code
        final_url = exc.geturl()
    except urllib.error.URLError as exc:
        return "unknown", str(exc.reason)
    except TimeoutError:
        return "unknown", "timeout"

    if status in {200, 301, 302, 303, 307, 308, 401, 403}:
        return "likely_taken_or_blocked", f"HTTP {status} {final_url}"
    if status == 404:
        return "public_page_missing", "HTTP 404; not proof of availability"
    return "needs_manual_check", f"HTTP {status} {final_url}"


def check_dns(domain: str) -> tuple[str, str]:
    try:
        socket.getaddrinfo(domain, None)
    except socket.gaierror as exc:
        if exc.errno == socket.EAI_NONAME:
            return "no_dns_record", "May be available; verify with registrar"
        return "unknown", str(exc)
    return "dns_resolves", "Likely registered or configured"


def iter_domain_results(names: Iterable[str], tlds: Iterable[str]) -> Iterable[ProbeResult]:
    for name in names:
        base = slugify_domain(name)
        if not base:
            continue
        for tld in tlds:
            domain = f"{base}{tld if tld.startswith('.') else '.' + tld}"
            signal, detail = check_dns(domain)
            yield ProbeResult(domain, "domain_dns", signal, detail)


def iter_social_results(
    names: Iterable[str], platforms: Iterable[str], limit: int, timeout: float
) -> Iterable[ProbeResult]:
    for name in names:
        for handle in candidate_handles(name, limit):
            for platform in platforms:
                pattern = PLATFORMS[platform]
                url = pattern.format(handle=handle)
                signal, detail = check_http(url, timeout)
                yield ProbeResult(f"{platform}:{handle}", "social_public_url", signal, detail)


def print_markdown(results: list[ProbeResult]) -> None:
    print("| Target | Type | Signal | Detail |")
    print("|---|---|---|---|")
    for result in results:
        detail = result.detail.replace("|", "\\|")
        print(f"| {result.target} | {result.kind} | {result.signal} | {detail} |")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="Brand names to probe")
    parser.add_argument(
        "--platforms",
        nargs="+",
        default=["instagram", "tiktok", "x", "threads", "youtube", "pinterest"],
        choices=sorted(PLATFORMS),
    )
    parser.add_argument("--domains", nargs="+", default=[".com", ".co", ".studio"])
    parser.add_argument("--handle-limit", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=6.0)
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    args = parser.parse_args()

    results = list(iter_domain_results(args.names, args.domains))
    results.extend(
        iter_social_results(args.names, args.platforms, args.handle_limit, args.timeout)
    )

    if args.json:
        print(json.dumps([asdict(result) for result in results], indent=2))
    else:
        print_markdown(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
