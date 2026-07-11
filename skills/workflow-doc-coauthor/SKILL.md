---
name: workflow-doc-coauthor
description: Turn operational knowledge into durable docs, SOPs, PRDs, decision records, status briefs, and handoff guides. Use when the user wants to document a workflow, write a spec, capture a decision, create a project handoff, prepare a concise update, or convert a repeated Codex/Notion/GitHub process into something reusable.
---

# Workflow Doc Coauthor

Use this skill to create docs that make future execution easier. The output should reduce monitoring burden, clarify ownership, and make the next run safer.

## Workflow

1. Identify the doc type:
   - SOP / runbook
   - PRD / implementation spec
   - decision record
   - status update
   - incident or blocker report
   - handoff guide
2. Gather only the context needed:
   - goal
   - current state
   - source of truth
   - owners
   - gates and constraints
   - success checks
   - known blockers
3. Draft for action:
   - Start with the operational answer.
   - Use concrete paths, commands, statuses, and field names.
   - Separate facts, decisions, assumptions, and open questions.
   - Avoid broad background unless it changes execution.
4. Verify claims against local files, repo config, Notion/database state, or official docs when behavior may have changed.
5. Save docs in the repo when the user wants future reuse.

## Defaults

- Match the audience's language and register for audience-facing copy; English is fine for internal technical docs unless the user asks otherwise.
- Treat workflow/tracker fields (e.g. Notion) as gates, not suggestions.
- Do not imply publish/upload/schedule/DM/final approval unless explicitly approved.
- Prefer machine-readable blockers and next actions over long narrative.

## Common Formats

Read `references/doc-patterns.md` for compact templates.

## Output Rules

- If editing repo docs, make scoped changes and preserve existing style.
- If writing a status brief, lead with what changed, what is blocked, and what the user needs to decide.
- If writing an SOP, include exact commands and validation checks.
- If writing a PRD, include non-goals and operational constraints.
