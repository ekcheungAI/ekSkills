# Firecrawl Web Agent Reference

Source studied: `firecrawl/web-agent` README and `agent-core` examples.

## Setup

Use the Firecrawl CLI for full agent projects:

```bash
npx -y firecrawl-cli@latest init -y --browser
firecrawl create agent -t next
firecrawl create agent -t express
firecrawl create agent -t library
```

For library use, install the agent core stack in a Node 20+ project and keep secrets in environment variables:

```bash
export FIRECRAWL_API_KEY="fc-..."
```

Do not commit the key.

## Agent-Core Mental Model

Firecrawl Web Agent combines:

- Firecrawl tools: search, scrape, interact, map, crawl, extract.
- Deep Agents: planning loop, subagents, skills, filesystem.
- Utility tools: structured output, bash processing, exportable skills.

Use it when the research task benefits from search-plus-scrape, autonomous page interaction, multiple independent workers, or JSON output.

## Basic Library Shape

```ts
import { createAgent } from "@firecrawl/agent-core";

const agent = createAgent({
  firecrawlApiKey: process.env.FIRECRAWL_API_KEY!,
  model: { provider: "google", model: "gemini-3-flash-preview" },
});

const result = await agent.run({
  prompt: "Collect source-backed evidence for the research question.",
  format: "json",
  schema: {
    type: "object",
    properties: {
      topic: { type: "string" },
      findings: { type: "array" },
      sources: { type: "array" }
    },
    required: ["topic", "findings", "sources"]
  }
});
```

## Subagent Pattern

Use subagents when each worker can finish independently:

- one company/product per worker;
- one source category per worker;
- one geography/language per worker;
- one known site per worker.

Avoid subagents when the work is sequential, the source count is small, or the workers would need to coordinate constantly.

Example shape:

```ts
await agent.run({
  prompt: "Compare the current AI video generation tools for creator workflows.",
  skills: ["deep-research", "competitor-analysis", "structured-extraction"],
  format: "json",
  subAgents: [
    {
      id: "official_docs",
      name: "Official Docs Analyst",
      description: "Extract facts from official product and docs pages.",
      instructions: "Use official domains first. Capture feature limits, dates, and URLs.",
      tools: ["search", "scrape"],
      maxSteps: 12
    },
    {
      id: "pricing",
      name: "Pricing Analyst",
      description: "Normalize pricing and quota details.",
      instructions: "Find pricing pages. Do not guess contact-sales prices.",
      tools: ["search", "scrape"],
      skills: ["pricing-tracker"],
      maxSteps: 12
    }
  ]
});
```

## Built-In Skill Ideas To Reuse

- `deep-research`: 3+ source triangulation and fact-checking.
- `structured-extraction`: scrape to an exact JSON schema.
- `competitor-analysis`: side-by-side product or company comparison.
- `pricing-tracker`: SaaS/API/cloud/LLM pricing normalization.
- `financial-research`: public-company filings and analyst consensus.
- `e-commerce`: product listings, variants, availability, pagination.

## Output Discipline

Before final output:

- verify all required schema fields are present;
- use `null` instead of omitting missing values;
- keep numbers as numbers, not strings;
- include exact source URLs;
- include `captured_at`;
- mark source confidence and contradictions.

## Credit Discipline

Search first without full-page extraction. Rank URLs, then scrape only pages that can change a claim or route decision. Set an explicit result limit and do not enable enhanced proxy or structured extraction unless the selected page requires it.

Stop on login walls, paywalls, terms restrictions, or access challenges. Firecrawl is not authorization to bypass a site's controls.
