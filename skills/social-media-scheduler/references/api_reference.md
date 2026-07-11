# Social Scheduler API Reference

## Credentials

Use environment variables. Never hard-code account tokens in skill files, scripts, or generated content.

```bash
export THREADS_ACCESS_TOKEN="..."
export UPLOAD_POST_API_KEY="..."
```

## Threads Direct API

Base URL: `https://graph.threads.net/v1.0`

Read-only checks:

- `GET /me?fields=id,username`
- `GET /me/threads_publishing_limit`

Immediate publish flow:

1. Create a media container:

```http
POST /me/threads
```

Common text parameters:

- `media_type=TEXT`
- `text=<post text>`

2. Publish the container:

```http
POST /me/threads_publish
```

Common parameters:

- `creation_id=<container id>`

Notes:

- Direct Threads publish is immediate. For future scheduling, use Upload-Post `scheduled_date` or a Codex automation that calls the direct publish flow later.
- All write actions require explicit user approval immediately before execution.

## Upload-Post API

Base URL: `https://api.upload-post.com/api`

Authentication:

```http
Authorization: Apikey <UPLOAD_POST_API_KEY>
```

Useful endpoints:

- `GET /uploadposts/me` - validate API key and account.
- `POST /upload_text` - publish or schedule text posts.
- `POST /upload_photos` - publish or schedule photos/carousels.
- `POST /upload` - publish or schedule videos.
- `GET /uploadposts/status?job_id=<job_id>` - scheduled job/upload status.
- `GET /uploadposts/history` - upload history.

Text scheduling parameters:

- `user` - Upload-Post user/profile identifier.
- `platform[]` - one or more of `threads`, `x`, `linkedin`, `facebook`, `reddit`, `bluesky`, etc.
- `title` - default text content.
- `scheduled_date` - ISO-8601 future date/time. Omit for immediate upload.
- `timezone` - IANA timezone, use `Asia/Hong_Kong` by default.
- `first_comment` - optional; on Threads and X this creates a reply/thread.

Expected scheduled response:

```json
{
  "success": true,
  "job_id": "scheduler_job_789",
  "scheduled_date": "2026-05-12T09:00:00+08:00"
}
```

## Approval Checklist

Before any publish/schedule request, show the user:

- Target account/profile.
- Target platforms.
- Final post text and media.
- Scheduled date/time with timezone, or "publish now".
- Whether first comment/reply threading is enabled.

Proceed only after the user explicitly approves.
