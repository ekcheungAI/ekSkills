---
name: agent-roster
description: Use when you want a second perspective from a specialist role — product-manager, ux-researcher, ui-designer, ui-finish-gate-reviewer, software-architect, workflow-architect, codebase-onboarding-engineer, code-reviewer, ai-code-security-auditor, or reality-checker — inside a Claude Code or Codex session. Ten adapted advisory personas: a brief before building, a design review, an architecture decision record, an onboarding walkthrough, a mid-work code review, a security pass, or independent verification that a feature actually works. None of them edit production code, ship, merge, or gain new tool access — they only change perspective and deliverables.
---

# Agent roster — ten extra helping roles

Ten adapted specialist roles, each a one-page `profile.md` plus a thin generated wrapper
per platform. They are **additive**: nothing here replaces your agent's built-in behavior,
changes a setting, grants a tool, or runs unless you call it. A role changes perspective and
deliverables; it never adds permissions.

| Group | Role | Call it for | Never |
|---|---|---|---|
| PM | `product-manager` | brief + work packages from a clear ask | scoping conversations, editing code |
| UX/UI | `ux-researcher` | friction findings with evidence tags, next research | inventing users out of thin air |
| UX/UI | `ui-designer` | implementable UI direction inside your brand system | production code |
| UX/UI | `ui-finish-gate-reviewer` | specificity/finish review of the running UI | fixing, deciding ship |
| Structure | `software-architect` | options + tradeoffs + ADR for a bounded question | implementing |
| Structure | `workflow-architect` | full workflow tree, handoffs, observable states | implementing |
| Structure | `codebase-onboarding-engineer` | cited orientation to an unfamiliar repo | editing |
| Review | `code-reviewer` | mid-work mentoring review of a diff | being the merge gate |
| Review | `ai-code-security-auditor` | CWE-mapped audit of agent-written code | changing creds/allowlists, attacks |
| Review | `reality-checker` | run the claim, report verified/not/broken | fixing, stopping other people's servers |

## Install

Copy this whole skill folder into your agent's skills directory, e.g.:

```bash
cp -R agent-roster ~/.claude/skills/    # or ~/.codex/skills/
```

## How to call a role

- **Claude Code**: ask for the role by name — "use the `reality-checker` agent on this PR",
  or `@"reality-checker (agent)"`. The files in `claude/` are what
  `~/.claude/agents/<slug>.md` (copy or symlink them there) exposes as a sub-agent. Each
  description says "use only when explicitly asked", so a role is never auto-picked by
  delegation — you have to name it.
- **Codex**: custom agent names use underscores (`reality_checker`). Copy `codex/*.toml`
  into `~/.codex/agents/`. Depth-1 delegation must be allowed in `config.toml`.
- **Any other agent runtime**: read `<slug>/profile.md` directly and act as that role for
  the current turn — that file is the entire operating instructions.

Give the role the same brief you would give a person: goal, what to look at, what shape you
want back. It reads its `profile.md` first; you get the deliverables the profile lists.

## Editing or adding a role

See `README.md` for the full editing workflow, upstream attribution, and license notes.
