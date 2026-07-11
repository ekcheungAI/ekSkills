# Instagram-Safe Collection

## Boundary

Use TikHub for public Instagram profiles, posts, reels, and comments. Use Scrapling only on public creator-owned pages such as personal sites, link-in-bio pages, course pages, newsletters, or product pages.

Stop collection when a source returns:

- HTTP 401, 403, or 429;
- private-account or login-required state;
- paywall, robots/terms restriction, or anti-bot challenge;
- a request for cookies, session data, or authentication.

Do not retry Instagram directly, solve challenges, reuse browser cookies, or probe private endpoints.

## Creator-Owned Page Flow

1. Start with the public profile or user-provided URL.
2. Extract creator-owned links.
3. Use static Scrapling on allowed pages.
4. Use JavaScript rendering only when the page is public and static extraction is empty.
5. Stop when blocked and record the coverage gap.
6. Normalize positioning, content pillars, lead magnets, paid offers, CTA language, proof, and limitations.

## Study Questions

- What identity or wedge does the creator own?
- What operator outcome do they promise?
- Which formats and hooks repeat?
- What proof and artifacts do they show?
- What audience objections appear in public comments?
- What can you adapt without copying wording, structure, or assets?

Never download full account histories or media by default. Use the smallest recent sample that answers the research question.
