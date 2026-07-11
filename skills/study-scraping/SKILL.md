---
name: study-scraping
description: Use when public web or social evidence must be collected at scale, including creator studies, transcripts, comments, pricing pages, competitor scans, repeatable crawls, or normalized research packets.
---

# Study Scraping

## Purpose

Collect public evidence as normalized `research.v1` cards. This skill owns extraction, pagination, retries, budgets, and metadata. Hand packets to a downstream topic-research or analysis step for confidence scoring and routing.

Keep raw titles, captions, quotes, handles, dates, IDs, metrics, and URLs in their source language. Never store tokens, cookies, private data, or full licensed content in a packet.

## Tool Router

1. Use normal web search or connectors for a few known pages.
2. Use TikHub for public Instagram, YouTube, or Reddit profiles, posts, videos, transcripts, comments, creator mechanics, and audience language.
3. Use Firecrawl to discover web sources, then scrape only selected URLs that can change the research decision.
4. Use Scrapling for allowed static/JavaScript pages when local targeted extraction or a repeatable spider is needed.
5. Stop on robots/terms restrictions, login walls, private content, paywalls, HTTP 401/403/429, or anti-bot challenges. Do not bypass them.

Read [tikhub-social-api.md](references/tikhub-social-api.md) for routes and normalized fields. Read [firecrawl-web-agent.md](references/firecrawl-web-agent.md) for broad web collection. Read [scrapling-local-extraction.md](references/scrapling-local-extraction.md) for allowed local extraction. For Instagram boundaries, read [instagram-safe-scrapling-extension.md](references/instagram-safe-scrapling-extension.md).

## Collection Contract

Every run starts with:

- one research question;
- a source/platform choice;
- `--limit`;
- `--page-budget`;
- `--deep-fetch-limit`.

Stop when fields are filled or budget is reached. Deep-fetch transcripts/comments only when they change a claim or decision.

Output must follow the `research.v1` packet shape emitted by the collector (see the normalized fields in [tikhub-social-api.md](references/tikhub-social-api.md)). A collection-layer packet normally uses `route: research_more` and leaves final claims/routing to a downstream analysis step.

## TikHub CLI

Store the token only as `TIKHUB_API_KEY` in `.env.local` or the shell environment.

Run commands from the skill folder (paths are relative to it):

```bash
python3 scripts/study_sources.py check-env
python3 scripts/study_sources.py tikhub-endpoints youtube/web_v2
python3 scripts/study_sources.py youtube-search "AI agent workflow" --limit 5 --page-budget 1
python3 scripts/study_sources.py youtube-video VIDEO_ID --limit 1
python3 scripts/study_sources.py instagram-profile creator_handle --limit 1
python3 scripts/study_sources.py instagram-posts creator_handle --limit 12 --page-budget 2 --deep-fetch-limit 3
python3 scripts/study_sources.py reddit-search "AI agent workflow" --limit 10
```

Use `tikhub-get` only for current public Instagram/YouTube/Reddit routes confirmed through `tikhub-endpoints`. The collector blocks login, cookie, session, private, inbox, and messaging paths.

TikHub defaults: bearer authentication, 45-second timeout, maximum three retries for transient server/network failures, and at most 10 requests per second. HTTP 401/403/429 stops immediately.

## Firecrawl Discipline

1. Search without scraping.
2. Rank results for primary-source value and relevance.
3. Scrape only selected URLs.
4. Capture the exact URL, publication/update date, extraction time, and evidence limitation.

Do not enable full-content scraping across every search result by default. Firecrawl search and per-page extraction both consume credits.

## Quality Gates

- Public source and permitted route.
- Stable source URL or platform ID.
- Original author/channel and publication date when available.
- Numeric metrics remain numbers.
- Raw evidence is kept separate from any later interpretation or analysis.
- Missing fields use `null` or a coverage note; never invent values.
- Provider failures stay visible in `coverage.provider_errors`.
- No publishing, scheduling, upload, DM, final approval, or Notion write without explicit permission.
