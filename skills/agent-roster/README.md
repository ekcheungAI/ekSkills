# Agent roster — extra helping roles

Ten adapted specialist roles from [Agency Agents](https://github.com/msitarzewski/agency-agents)
(`ad9264e`, MIT — see `UPSTREAM-LICENSE`). Each role is one `profile.md` here plus a thin
generated wrapper per platform (`claude/`, `codex/`). They are **additive**: nothing here
replaces a built-in Claude Code or Codex agent, changes a setting, grants a tool, or runs
unless called. A persona changes perspective and deliverables; it never adds permissions.

See `SKILL.md` for the install and call instructions. This file covers editing and provenance.

| Group | Role | Call it for | Never |
|---|---|---|---|
| PM | `product-manager` | brief + work packages from a clear ask | scoping conversations, editing code |
| UX/UI | `ux-researcher` | friction findings with evidence tags, next research | inventing users (use a persona-simulation workflow if you have one) |
| UX/UI | `ui-designer` | implementable UI direction inside the brand system | production code |
| UX/UI | `ui-finish-gate-reviewer` | specificity/finish review of the running UI | fixing, deciding ship |
| Structure | `software-architect` | options + tradeoffs + ADR for a bounded question | implementing |
| Structure | `workflow-architect` | full workflow tree, handoffs, observable states | implementing |
| Structure | `codebase-onboarding-engineer` | cited orientation to an unfamiliar repo | editing |
| Review | `code-reviewer` | mid-work mentoring review of a diff | your project's merge-gate reviewer, if it has one |
| Review | `ai-code-security-auditor` | CWE-mapped audit of agent-written code | changing creds/allowlists, attacks |
| Review | `reality-checker` | run the claim, report verified/not/broken | fixing, stopping others' servers |

## Editing

1. Edit `roster.json` (description = the routing contract) and/or `<slug>/profile.md`.
2. `python3 scripts/build_agent_roster.py` to regenerate `claude/*.md` and `codex/*.toml`.
3. `python3 scripts/build_agent_roster.py --check` before committing — confirms wrappers are
   current, slugs are kebab-case, and every profile file exists.

Adding a role: pick one from [Agency Agents](https://github.com/msitarzewski/agency-agents),
add a `roster.json` entry, write an adapted `profile.md` (keep Identity / Job / Critical
rules / Workflow / Deliverables / Communication / Boundaries, with an upstream attribution
line at the top), strip stack-specific gates and fixed verdicts so it stays portable across
projects, regenerate.

## Provenance

All ten profiles are adapted, not copied verbatim — upstream's fixed tech-stack gates (e.g.
Laravel/Playwright specifics) and hard-coded verdicts were replaced with plain
evidence-based reporting, and each profile's `Boundaries` section is original. Each
`profile.md` names its exact upstream source file at the top. Upstream is MIT-licensed;
`UPSTREAM-LICENSE` is its license text, kept alongside this adaptation per its terms.
