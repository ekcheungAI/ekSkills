---
name: mcp-server-builder
description: Design, implement, review, or debug Model Context Protocol servers for Codex workflows. Use when building a custom MCP server, choosing MCP tools/resources/prompts, wrapping an external API, exposing a database or internal service to agents, hardening MCP auth/secrets handling, or converting a repeated connector workflow into a reusable server.
---

# MCP Server Builder

Use this skill when a normal script is no longer enough and Codex needs a reusable tool surface for an external service, database, or internal workflow.

## Decision Rule

Build an MCP server only when it creates durable leverage:

- Multiple workflows need the same API or data source.
- Tool inputs/outputs can be made structured and stable.
- Authentication can be handled through environment variables or connector infrastructure.
- The user benefits from a reusable tool instead of one-off shell scripts.

Do not build an MCP server when a short local script, existing connector, or official plugin already solves the problem.

## Workflow

1. Inspect the target repo and existing connectors first.
2. Define the real user tasks before naming tools.
3. Choose the minimum useful surface:
   - `tools`: actions or queries with structured inputs.
   - `resources`: stable documents, schemas, logs, or database snapshots.
   - `prompts`: reusable task templates only when they reduce repeated setup.
4. Design tool schemas around task intent, not raw API endpoints.
5. Keep auth out of code:
   - Read secrets from environment variables, local env files, or secure connector auth.
   - Never print tokens in logs.
   - Provide `.env.example` only.
6. Implement the smallest working server.
7. Add deterministic smoke tests for tool schema, missing auth, and one successful mocked or dry-run call.
8. Document how Codex should start or connect to the server.

## Tool Design Rules

- Prefer fewer, higher-level tools that map to actual decisions or workflow steps.
- Make destructive actions explicit and gated.
- Use enums for states, database names, project names, and workflow gates when possible.
- Return machine-readable blockers instead of vague failures.
- Include source IDs, URLs, or timestamps when the result may be used as evidence.
- Make dry-run support the default for external writes whenever practical.

## Content-pipeline MCP rules (example domain)

For a content/publishing pipeline MCP, a good gating pattern:

- Treat workflow statuses (e.g. Notion) as hard gates.
- Do not publish, upload, schedule, DM, or mark final approval without explicit approval.
- Encode blockers such as missing public asset URL, missing approval, duplicate schedule risk, or claim-safety failure as structured fields.
- Prefer existing connectors (Notion/GitHub/Cloudflare/…) before building a new raw MCP server.

## References

Read `references/codex-mcp-patterns.md` before designing the server API.
