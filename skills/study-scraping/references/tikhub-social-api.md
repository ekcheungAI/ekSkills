# TikHub Social API

Use TikHub for public platform-native evidence that changes a research decision: creator mechanics, captions, transcripts, comments, public metrics, audience objections, or outlier references.

TikHub is a signal/evidence collector, not proof for pricing, policy, product access, model benchmarks, legal claims, or roadmaps. Verify those with official primary sources.

## Runtime

- OpenAPI: `https://api.tikhub.io/openapi.json`
- Default base URL: `https://api.tikhub.io`
- Mainland China base URL: `https://api.tikhub.dev`
- Credential: `TIKHUB_API_KEY`
- Header: `Authorization: Bearer <token>`
- Timeout: 45 seconds by default
- Retry: maximum 3 for transient network/5xx errors
- Rate: maximum 10 QPS

Set `TIKHUB_API_BASE=https://api.tikhub.dev` only when running from Mainland China. Never put the token in a command, URL, skill file, or output.

## Supported High-Level Commands

Run from the skill folder (paths are relative to it):

```bash
python3 scripts/study_sources.py tikhub-endpoints instagram/v3
python3 scripts/study_sources.py youtube-search "AI tutorial" --limit 5
python3 scripts/study_sources.py youtube-video VIDEO_ID --limit 1
python3 scripts/study_sources.py instagram-profile HANDLE --limit 1
python3 scripts/study_sources.py instagram-posts HANDLE --limit 12 --page-budget 2
python3 scripts/study_sources.py reddit-search "AI workflow" --limit 10
```

Current route mapping:

| Command | TikHub route |
| --- | --- |
| `youtube-search` | `/api/v1/youtube/web_v2/get_general_search` |
| `youtube-video` | `/api/v1/youtube/web_v2/get_video_info` |
| `instagram-profile` | `/api/v1/instagram/v3/get_user_profile` |
| `instagram-posts` | `/api/v1/instagram/v3/get_user_posts` |
| `reddit-search` | `/api/v1/reddit/app/fetch_dynamic_search` |

Inspect the current OpenAPI before adding or changing a repeatable route.

## Generic Public Route

Use only after endpoint inspection:

```bash
python3 scripts/study_sources.py \
  tikhub-get /api/v1/youtube/web_v2/get_video_comments \
  --platform youtube \
  --operation comments \
  --param video_id=VIDEO_ID \
  --limit 20 \
  --page-budget 1 \
  --deep-fetch-limit 1
```

The generic route accepts public Instagram, YouTube, and Reddit paths only. Login, cookie, session, inbox, private, and messaging paths are blocked.

## Platform Guidance

YouTube:

- Start with search or a known video ID.
- Use public stats for demand; use captions/comments only when they change the teaching steps or objections.
- Keep the official YouTube Data API as the authoritative discovery/stats layer for any downstream analysis step.

Instagram:

- Fetch profile once, then a bounded recent-post sample.
- Deep-fetch only top posts.
- Stop immediately on private/login/access errors.

Reddit:

- Search posts for operator pain and objections.
- Default to `safe_search=strict` and `allow_nsfw=0`.
- Treat comments as audience language, not independent factual verification.

## Normalized Output

The collector returns `research.v1` with TikHub source cards containing collector, platform, public URL, title/caption, author, publication date, numeric metrics, signal evidence role, confidence, and an auditable raw reference containing IDs rather than full payloads.

Keep full responses out of content handoffs unless a specific field cannot otherwise be audited.
