# Codex MCP Patterns

## Useful Server Shapes

### Query Adapter

Use when Codex needs read-heavy access to a service.

Examples:

- Search research rows with normalized status fields.
- Fetch current automation health.
- Read public asset metadata from storage.

Tool shape:

```json
{
  "query": "string",
  "filters": {"status": "Image Review"},
  "limit": 10
}
```

Return IDs, titles, timestamps, URLs, status fields, and blocker fields.

### Workflow Gatekeeper

Use when the server decides whether an action is allowed.

Examples:

- Check if a Social Posts row can move from `Image Review` to `Ready for Posting`.
- Check if a scheduler may call an external upload API.

Return:

```json
{
  "allowed": false,
  "blocker_type": "Missing Public Asset URL",
  "next_action": "Create a durable hosted preview URL before promotion."
}
```

### Dry-Run Writer

Use when writes are allowed but need previewable changes.

Inputs should include:

- `dry_run`: default `true`
- target ID
- requested transition/action
- idempotency key when calling external APIs

Outputs should include planned field changes, external calls that would be made, and blockers.

## Implementation Notes

- Start with a local server and mocked API responses.
- Add live API calls only after the schema is stable.
- Include timeouts and concise error messages.
- Avoid hidden retries for write tools; retries can create duplicates.
- Keep logs useful but secret-free.

## Smoke Test Matrix

Every MCP project should have a basic check for:

- Server starts.
- Tool list is valid.
- Missing auth produces a clear error.
- Dry-run write does not call external services.
- One happy-path read or mocked write returns the documented structure.
