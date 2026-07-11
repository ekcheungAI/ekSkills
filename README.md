# ekSkills

@ekcheungAI 特別技能庫 — dedicated Git home for the special / high-value Claude Code
skills that deserve their own repo (production-patched engines, hard-won pipelines),
separate from the general `ekcheungai/codex-skills` mirror.

## Skills

| Skill | What it does |
|---|---|
| [`ekcheungai-scroll-world`](skills/ekcheungai-scroll-world/SKILL.md) | Scroll-scrubbed "fly through the world" cinematic landing pages (the ekcheung.com brandflush homepage effect). Clone of the scroll-world plugin v0.1.3 (MIT) + production patches: iOS decoder-slot release, final-scene hold, site-nav coordination pattern. |

## Install / use

The live skill store on the main machine is `~/Desktop/ekOS/00_ekos/skills/`
(`~/.claude/skills` and `~/.codex/skills` are symlinks to it). To use a skill from
this repo on another machine, copy its folder into that machine's skill directory:

```bash
cp -R skills/ekcheungai-scroll-world ~/.claude/skills/
```

## Sync rules

- **Source of truth for skill content:** the live store (`00_ekos/skills/`). Edit
  there, then copy the updated folder into this repo and commit.
- **Source of truth for the scrub engine:** the ekcheung.com repo
  (`js/scrub-engine.js`). If it changes, re-mirror into the skill's
  `references/scrub-engine.js` everywhere.
- No secrets in this repo — ever. Skills must reference env vars, not values.

## License

Each skill folder carries its own LICENSE where it adapts third-party work
(e.g. scroll-world is MIT, © 2026 cyw). Everything else © Elvin Cheung.
