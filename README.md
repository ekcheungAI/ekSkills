# ekSkills

A small, curated set of **Agent Skills** by [@ekcheungAI](https://github.com/ekcheungAI) —
published so others can **use them and learn from them**.

Every skill here is a self-contained `SKILL.md` (plus optional `references/`, `scripts/`,
`agents/`). They follow the portable Agent-Skill format, so they work across Claude Code,
Codex CLI, Cursor, and any compatible agent runtime.

This repo is a *curated* selection, not a dump — only original skills, cleaned of any
private/brand-specific coupling, so each one is genuinely reusable on your own projects.

## Skills

| Skill | What it does | What you'll learn |
|---|---|---|
| [`scroll-world`](skills/scroll-world/) | Scroll-scrubbed "fly through the world" cinematic landing pages (Higgsfield). | Building a scroll-driven camera-flight page with seamless seams, plus real iOS/mobile video-decoder fixes. Adapts the scroll-world plugin (MIT) with two production patches. |
| [`website-design`](skills/website-design/) | Modern web/UI design direction for landing pages, SaaS, portfolios. | A repeatable method for current, non-generic web design: design theses, dials, pattern stacks, and an anti-AI-slop QA pass. |
| [`goal-setter`](skills/goal-setter/) | Turns a vague ask into a bounded, checkable task contract. | A reusable framework for scoping agent work so it stays on-rails and verifiable. |
| [`brand-name-search`](skills/brand-name-search/) | Evaluates brand names, domains, and social handles. | A screening workflow (with a probe script) for finding an ownable, available name. |
| [`cinematic-photo-prompts`](skills/cinematic-photo-prompts/) | Documentary "non-AI-looking" photo-prompt craft. | Lens, blocking, and lighting recipes that make generated stills read like real photographs. |
| [`study-scraping`](skills/study-scraping/) | Public-web/social research-collection pipeline. | A structured, rate-limit-aware approach to collecting and studying source material at scale. |
| [`mcp-server-builder`](skills/mcp-server-builder/) | Design and debug MCP (Model Context Protocol) servers. | Tool-API design principles: high-level tools, gated destructive actions, machine-readable blockers. |
| [`workflow-doc-coauthor`](skills/workflow-doc-coauthor/) | Co-author SOPs, PRDs, and decision records. | Writing operational docs that lead with the answer and separate facts, decisions, and open questions. |
| [`social-media-scheduler`](skills/social-media-scheduler/) | Draft and schedule posts to Threads/IG/X. | Wiring an agent to social APIs safely, with env-var tokens and dry-run-first defaults. |
| [`minimax-m3-audio`](skills/minimax-m3-audio/) | MiniMax M3 chat + text-to-speech via the API. | A clean wrapper pattern for an OpenAI-compatible LLM + TTS provider, keyed entirely by env vars. |
| [`aihot`](skills/aihot/) | Queries a public AI-news REST API for a Chinese-language digest. | A model example of a **no-MCP, curl-a-public-API** skill — no keys, no server, just HTTP. |

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
