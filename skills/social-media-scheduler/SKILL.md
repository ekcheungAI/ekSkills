---
name: social-media-scheduler
description: Provides comprehensive guidance and workflows for drafting, scheduling, and publishing social media posts with images across multiple platforms (Threads, Instagram, X). Use this skill for any social media content creation and scheduling tasks, ensuring proper image attachment and adherence to platform-specific best practices.
---

# Social Media Scheduler Skill

This skill is designed to streamline the process of creating, scheduling, and publishing engaging social media content, complete with image attachments, across various platforms such as Threads, Instagram, and X (Twitter).

## Overview

Leveraging the Upload-Post API, this skill automates the workflow from content drafting to scheduled publication, ensuring consistency and efficiency in your social media strategy. It incorporates best practices for each platform and handles image integration seamlessly.

## API Access Model

- **Threads direct API**: Use Meta Threads API for read checks, publishing-limit checks, and immediate publish flows through `https://graph.threads.net/v1.0`. Requires `THREADS_ACCESS_TOKEN` in the environment. Direct publish is a two-step create-container then publish flow.
- **Upload-Post API**: Use Upload-Post for scheduling and multi-platform distribution through `https://api.upload-post.com/api`. Requires `UPLOAD_POST_API_KEY` in the environment and connected social profiles in Upload-Post.
- **Scheduling rule**: Prefer Upload-Post `scheduled_date` for scheduled posts. Use direct Threads API only for immediate publish unless the user explicitly asks to schedule via a Codex automation that publishes later.
- **Safety rule**: Never publish, schedule, delete, DM, or start AutoDM monitors without showing the final content, target platform/account, and exact scheduled time, then receiving explicit user approval.

## Core Capabilities

- **Multi-Platform Publishing**: Draft and publish content to Threads, Instagram, and X simultaneously or selectively.
- **Image Attachment**: Ensures images are correctly attached and processed for each platform.
- **Scheduled Posting**: Allows precise scheduling of posts for optimal timing and audience engagement.
- **Content Tailoring**: Guides the creation of platform-specific content, including hashtag management and character limits.
- **Error Handling**: Provides mechanisms to detect and report API errors during publication.

## Workflow for Social Media Posting

1.  **Content Drafting**: Prepare the text content for each platform (Threads, Instagram, X), considering their unique requirements.
    - Threads: no hashtags.
    - Instagram: maximum 3 hashtags.
    - X: keep hashtags optional and sparse; prioritize clarity over tag stuffing.
2.  **Image Preparation**: Ensure the image is ready for upload. The skill will handle the attachment process.
3.  **Scheduling**: Specify the desired publication date and time (e.g., Saturday morning 9 AM HKT).
4.  **Preview and Approval**: Review the drafted posts and scheduled time before final confirmation.
5.  **Automated Publication**: The skill will use the Upload-Post API to publish the content at the scheduled time.

## Helper Script

Use `scripts/social_scheduler.py` for read-only access checks and for preparing Upload-Post schedule requests. It defaults to dry-run for posting actions. Required environment variables:

```bash
export THREADS_ACCESS_TOKEN="..."
export UPLOAD_POST_API_KEY="..."
```

Examples:

```bash
python scripts/social_scheduler.py check-threads
python scripts/social_scheduler.py check-upload-post
python scripts/social_scheduler.py schedule-upload-text --user yourhandle --platform threads --text "Draft post" --scheduled-date "2026-05-12T09:00:00+08:00" --timezone Asia/Hong_Kong
```

Only add `--execute` after explicit approval from the user.

## Usage Scenarios

- Scheduling daily or weekly social media updates.
- Launching marketing campaigns across multiple platforms.
- Automating content distribution for blogs or news updates.
- Ensuring consistent branding and messaging across social media channels.

## Important Notes

- **API Key**: A valid Upload-Post API key is required for publication. Ensure it is up-to-date.
- **Threads Token**: A valid Threads access token is required for direct Threads checks/publishing. Do not hard-code it in this skill or scripts.
- **Image Requirements**: Adhere to platform-specific image guidelines for best results.
- **Timezone**: Always specify `Asia/Hong_Kong` for accurate scheduling in Hong Kong time.

This skill aims to simplify your social media management, allowing you to focus on content quality and audience engagement.
