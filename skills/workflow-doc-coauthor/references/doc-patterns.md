# Doc Patterns

## SOP / Runbook

```markdown
# [Workflow Name]

## Purpose
[What this workflow accomplishes.]

## Source Of Truth
[Notion database, repo path, dashboard, API, or owner.]

## Gates
- [Status / approval / field requirement]

## Steps
1. [Action]
2. [Action]

## Validation
- [Command/check]

## Failure Modes
- `[Blocker Type]`: [what to do]
```

## Decision Record

```markdown
# Decision: [Name]

## Context
[Current situation.]

## Decision
[What we chose.]

## Why
[Short rationale.]

## Non-Goals
- [What this does not attempt.]

## Follow-Up
- [Concrete next action]
```

## Status Brief

```markdown
## Summary
[One paragraph.]

## Done
- [Concrete completed item]

## Blocked
- `[Blocker]`: [owner / next action]

## Needs Decision
- [Decision and options]
```

## Implementation Spec

```markdown
# [Feature / Workflow]

## Goal
[User-visible outcome.]

## Scope
- [Included]

## Non-Goals
- [Excluded]

## Data / State
- [Fields, statuses, tables, paths]

## Flow
1. [Step]

## Checks
- [Tests, scripts, dashboards]
```
