# ekSkills

A small, curated set of **Agent Skills** by [@ekcheungAI](https://github.com/ekcheungAI) —
published so others can **use them and learn from them**.

> 🇭🇰 中文介紹 + 我推薦嘅 skills（設計 / 動畫 / 編程 / 研究）：**[ekcheung.com/skills](https://www.ekcheung.com/skills/)**

Every skill here is a self-contained `SKILL.md` (plus optional `references/`, `scripts/`,
`agents/`). They follow the portable Agent-Skill format, so they work across Claude Code,
Codex CLI, Cursor, and any compatible agent runtime.

This repo is a *curated* selection, not a dump. Two parts:

1. **Our skills** — original work by @ekcheungAI, cleaned of any private/brand-specific
   coupling, so each one is reusable on your own projects.
2. **[Recommended skills](#recommended-skills-third-party)** — great skills by *other*
   authors that we use and endorse. We don't host their code; we link to the source and
   credit the maker. Go star their repos.

## Our skills

| Skill | What it does | What you'll learn |
|---|---|---|
| [`scroll-world`](skills/scroll-world/) | Scroll-scrubbed "fly through the world" cinematic landing pages (Higgsfield). | Building a scroll-driven camera-flight page with seamless seams, plus real iOS/mobile video-decoder fixes. Adapts the scroll-world plugin (MIT) with two production patches. |
| [`website-design`](skills/website-design/) | Modern web/UI design direction for landing pages, SaaS, portfolios. | A repeatable method for current, non-generic web design: design theses, dials, pattern stacks, and an anti-AI-slop QA pass. |
| [`goal-setter`](skills/goal-setter/) | Turns a vague ask into a bounded, checkable task contract. | A reusable framework for scoping agent work so it stays on-rails and verifiable. |
| [`cinematic-photo-prompts`](skills/cinematic-photo-prompts/) | Documentary "non-AI-looking" photo-prompt craft. | Lens, blocking, and lighting recipes that make generated stills read like real photographs. |
| [`study-scraping`](skills/study-scraping/) | Public-web/social research-collection pipeline. | A structured, rate-limit-aware approach to collecting and studying source material at scale. |

## Recommended skills (third-party)

Skills we reach for that we **didn't** write. These belong to their authors under their own
licenses — this is a recommendation list, not a re-host. Install them from the source.

### Design & UI
- **[taste-skill](https://github.com/Leonxlnx/taste-skill)** (Leonxlnx) and
  **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)**
  (nextlevelbuilder) — the anti-slop design system behind skills like `taste-skill`,
  `soft-skill`, `brutalist-skill`, `minimalist-skill`, `image-to-code`, `redesign`,
  `imagegen-frontend-web/-mobile`, `stitch`, `gpt-taste`. Our own `website-design` skill
  studied these; credit where due.

### Animation
- **[GSAP Skills](https://github.com/greensock/gsap-skills)** (GreenSock, official) — teaches
  agents to use GSAP correctly: timelines, ScrollTrigger, plugins, React/Vue. The go-to for web
  animation.

### Agent methodology & workflow
- **[superpowers](https://github.com/obra/superpowers)** (Jesse Vincent / obra) — the
  composable-skills framework that ships `brainstorming`, `test-driven-development`,
  `systematic-debugging`, `using-git-worktrees`, `writing-plans`, `subagent-driven-development`,
  the code-review skills, and more. The most-starred Claude Code skills repo, and deservedly so.

### Understand a codebase
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — turns any repo
  into an interactive knowledge graph (`understand`, `understand-chat`, `understand-dashboard`,
  and the rest of that family).

### Documents, browser & integrations
- **[anthropics/skills](https://github.com/anthropics/skills)** — Anthropic's official Agent
  Skills: `pdf`, `docx`, `pptx`, `xlsx`, the `playwright` browser toolkit, and the Apache-2.0
  example skills.
- **[Scrapling](https://github.com/D4Vinci/Scrapling)** (Karim Shoair, BSD-3) — adaptive web
  scraping with a built-in MCP server.
- **[Context7](https://github.com/upstash/context7)** (Upstash) — pulls up-to-date library
  docs into the agent's context.

### Skills Radar picks
<!-- skills-radar: recommendations -->
- **[trip-planner-skill](https://github.com/skywain/trip-planner-skill)** (skywain, MIT) — Agent skill for AI trip planning (Claude Code · Codex · Gemini CLI · Cursor · Copilot · any SKILL.md agent) — verified, bookable itineraries: hour-by-hour days, real flight prices, offline KML maps, eight themed page designs · 旅行规划 / 行程 / 机票比价
- **[Tlamatini](https://github.com/XAIHT/Tlamatini)** (XAIHT, MIT) — Tlamatini is a self-hosted AI developer assistant for local or cloud LLMs: hybrid RAG (FAISS+BM25) over your codebase, a 100+ tool Multi-Turn engine, an 86-agent visual workflow designer, 28 SKILL.md skills, a universal MCP client, and ACPX, a runtime for external coding agents like Claude Code, Codex, Cursor and Gemini CLI.
- **[skillhawk](https://github.com/Berserk-hub150/skillhawk)** (Berserk-hub150, MIT) — Catch dangerous AI agent skills before they catch you. Zero-dependency security scanner for Agent Skills, SKILL.md and MCP configs.
- **[seqcli](https://github.com/datalust/seqcli)** (datalust, Apache-2.0) — The Seq command-line client. Administer, log, ingest, search, from any OS.
- **[ai-conductor](https://github.com/jstoup111/ai-conductor)** (jstoup111, Apache-2.0) — Review the upstream SKILL.md before installation.
- **[open-design](https://github.com/nexu-io/open-design)** (nexu-io, Apache-2.0) — 本地優先嘅開源 design workspace，可用 Claude Code、Codex、Cursor 等 agent 產生多種設計資產。
- **[claude-codex-settings](https://github.com/fcakyon/claude-codex-settings)** (fcakyon, Apache-2.0) — 跨 Claude Code、Codex、Cursor 嘅 configs、plugins、hooks 同 agents 集合。
- **[agnix](https://github.com/agent-sh/agnix)** (agent-sh, Apache-2.0) — 檢查 AGENTS.md、CLAUDE.md、SKILL.md、hooks 同 MCP 嘅 linter／LSP。
- **[open-science](https://github.com/aipoch/open-science)** (aipoch, Apache-2.0) — 模型無關嘅開源科學研究工作台同生命科學 skills。
- **[lpm](https://github.com/gug007/lpm)** (gug007, MIT) — 集中啟動、停止同複製 agent 開發專案嘅 workspace。

### Built into your agent already
Skills like `create-hook`, `create-rule`, `create-skill`, `create-subagent`, `cursor-sdk`,
`migrate-to-skills`, `figma-implement-design`, `gh-fix-ci`, `gh-address-comments`, `yeet`,
`split-to-prs`, `sentry`, `vercel-deploy`, and `chronicle` ship **built in** with
[Cursor](https://cursor.com) / Claude Code — no separate install needed. Use them from there.

> Attribution note: these names are trademarks/works of their respective authors. If you
> maintain one of these and want the link changed or removed, open an issue.

## Using a skill

Copy the skill folder into your agent's skills directory. For example, Claude Code / Codex:

```bash
cp -R skills/website-design ~/.claude/skills/    # or ~/.codex/skills/
```

Then invoke it by name (e.g. `/website-design`) or let the agent auto-select it from the
`description` in its frontmatter.

Skills that call external APIs read their credentials from **environment variables** only —
never hardcode keys. Check each skill's `SKILL.md` for the exact env vars it expects.

## Notes

- **No secrets, ever.** Skills reference env vars, not values. If you find anything that looks
  like a credential, please open an issue.
- **`scroll-world`** is adapted from the upstream scroll-world plugin (MIT, © 2026 cyw) and
  carries that license in its own folder; `website-design` cites its trend sources in-file.
- Everything else is original work, MIT-licensed (see [`LICENSE`](LICENSE)).

## License

MIT © 2026 Elvin Cheung (@ekcheungAI). See [`LICENSE`](LICENSE). The `scroll-world` skill is
under its own MIT license (see `skills/scroll-world/LICENSE`).
