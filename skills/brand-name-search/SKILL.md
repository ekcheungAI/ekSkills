---
name: brand-name-search
description: Search and evaluate brand names, domains, and social media usernames for new brands, products, projects, character IPs, startups, campaigns, or account naming. Use when the user asks to check name availability, domain availability, Instagram/TikTok/X/YouTube/Threads/Pinterest handles, username options, naming conflicts, SEO conflicts, or to choose the best ownable brand name.
---

# Brand Name Search

## Overview

Use this skill to turn brand-name candidates into an ownability report: domain options, social handle options, public conflict signals, and a practical recommendation.

Do not treat public profile 404s as proof of availability. Social platforms may reserve, ban, or hide usernames. Present public checks as screening evidence and recommend final confirmation in the platform signup or username-change flow.

## Workflow

1. **Collect candidates**
   - Start from user-provided names, project files, or current naming context.
   - Generate 3-8 handle variants per strong candidate.
   - Prefer short, readable variants before adding suffixes.

2. **Normalize names**
   - Domains: lowercase, hyphen only when readability improves.
   - Handles: lowercase, no punctuation where possible.
   - Avoid confusing spelling, repeated letters, hard-to-say compounds, and names that require explanation.

3. **Check domains**
   - Use the Vercel domain availability tool when available for purchase availability and pricing.
   - Check `.com` first, then context-specific TLDs such as `.co`, `.studio`, `.world`, `.club`, `.shop`, `.app`, `.ai`, `.gg`, `.jp`, or local-market TLDs.
   - Treat non-`.com` names as acceptable only when the social handles are strong or the brand intentionally fits that TLD.

4. **Check social handles**
   - Use Browser/Chrome or web requests for public profile URLs.
   - Check priority platforms based on the brand type:
     - Character/IP: Instagram, TikTok, YouTube, Threads, Pinterest, LINE/Kakao search where relevant.
     - SaaS/app: X, GitHub, YouTube, LinkedIn, Product Hunt, app-store search.
     - Commerce: Instagram, TikTok, Pinterest, Etsy, Shopify, Amazon search.
   - If a profile resolves, inspect whether it is an active conflict, irrelevant inactive account, fan use, parked account, or possible impersonation risk.

5. **Search the open web**
   - Run exact-match searches for each finalist:
     - `"<name>"`
     - `"<name>" brand`
     - `"<name>" instagram`
     - `"<name>" tiktok`
     - `"<name>" character`
     - `"<name>" shop`
   - For high-stakes launches, add trademark or registry checks in relevant markets. Do not claim legal clearance unless a proper trademark search was performed.

6. **Score ownability**
   - Score each name from 1-5 on:
     - Domain strength
     - Social handle strength
     - Search distinctiveness
     - Pronunciation/memorability
     - Strategic fit
     - Conflict risk
   - Recommend 1-3 names, not a huge list.

## Candidate Generation

For each base name, create variants in this order:

1. Exact: `brandname`
2. Lightweight suffix: `brandnamehq`, `brandnameco`, `brandnamestudio`
3. Community/world suffix: `brandnameclub`, `brandnameworld`, `brandnamelife`
4. Product/category suffix: `brandnameshop`, `brandnameapp`, `brandnametv`
5. Official fallback: `brandnameofficial`

Avoid `real`, `theofficial`, long double suffixes, numbers, underscores, and platform-specific handles unless the exact name is unavailable everywhere.

## Script

Use `scripts/probe_brand_handles.py` for a first-pass public URL and DNS probe:

```bash
python3 scripts/probe_brand_handles.py "Moodlings" "Mizukuma" --domains .com .co .studio
```

The script is a screening tool only. Follow it with Vercel domain checks, Browser/Chrome profile inspection, and web search before making a recommendation.

## Output Format

Use this concise report shape:

```markdown
**Recommendation**
1. Name - why it is strongest
2. Name - why it is a backup

**Availability Snapshot**
| Name | Best Domain | Best Handle | Conflicts | Score |
|---|---|---|---|---|

**Notes**
- Domain availability:
- Instagram/TikTok/X/YouTube:
- Search conflicts:
- Risk:

**Next Step**
Reserve these exact domains/handles first: ...
```

## Decision Rules

- Prefer a name with exact social handles and a good alternate domain over a name with `.com` but messy social handles for social-first brands.
- Prefer `.com` for serious companies, paid products, and investor-facing projects.
- Prefer exact Instagram/TikTok handles for character IP, creator brands, fashion, food, and consumer products.
- Penalize names already used by a character, toy, game, crypto token, adult content account, app, or active shop.
- Penalize names whose Google results are dominated by unrelated high-authority entities.
- Flag spelling collisions, pronunciation ambiguity, and likely trademark issues separately from availability.
