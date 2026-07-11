# Inspiration Research

Use this reference when the task benefits from external examples, Mobbin MCP, image generation, or MotionSites-style prompt engineering.

## Research Order

1. Start with the user's product and conversion goal. Define what the reference search must answer: layout, interaction, onboarding, pricing, app UI, motion, visual mood, or hero impact.
2. Use Mobbin MCP when available for real product patterns, especially onboarding, paywalls, dashboards, forms, navigation, settings, search, commerce, and mobile-first flows.
3. Use web research for current public landing-page patterns, competitor positioning, and named designers/sites the user cites.
4. Use imagegen for fast visual divergence when the direction is still open or the user wants inspiration. Generate 2-4 different routes, then critique them before implementation.
5. Convert references into a new design system. Never copy a whole layout, brand, illustration, or proprietary prompt.

## Mobbin MCP Flow

When Mobbin tools are available:

- Search by product category first: fintech, AI assistant, productivity, creator tools, ecommerce, travel, health, education, enterprise SaaS.
- Search by interaction pattern second: onboarding, signup, empty state, pricing, search, dashboard, invite flow, upgrade, confirmation, settings.
- Extract only reusable design logic: information hierarchy, interaction states, form structure, progression, density, navigation model, component anatomy, and mobile behavior.
- Compare 3-5 examples before choosing a pattern. Avoid overfitting to one reference.
- Mention which product/category patterns influenced the design when summarizing.

If Mobbin MCP is configured but not exposed in the current tool list, state that it is unavailable in this session and continue with web/imagegen references.

## Imagegen Inspiration Loop

Use imagegen as exploration, not final truth.

1. Generate distinct visual routes from the same brief:
   - conservative premium
   - bold editorial
   - motion/cinematic
   - product-first conversion
2. Keep prompts implementation-aware: section job, grid, typography, material, imagery, CTA, states, and responsive intent.
3. Critique each image for hierarchy, feasibility, brand fit, contrast, and mobile implications.
4. Select one route or hybridize two. Translate the chosen route into concrete CSS/component decisions.
5. Do not preserve broken text, impossible geometry, unreadable overlays, or decorative artifacts from generated images.

## MotionSites / Viktor Oddy Lessons

Publicly visible MotionSites material shows a useful pattern: treat prompts like design specifications, not vague mood requests.

Adopt this structure:

- Product and industry.
- Exact hero goal.
- Design system tokens: colors, type, radius, spacing, surfaces, shadows.
- Layout structure: navbar, hero grid, visual area, CTA cluster, proof row, logo marquee if real.
- Typography specs: approximate sizes, weights, line-height, tracking, responsive steps.
- Motion specs: entrance timing, hover states, scroll behavior, video/background behavior, reduced-motion fallback.
- Component specs: buttons, cards, media frames, badges, panels, forms, and states.
- Implementation stack: React, Next.js, Tailwind, Framer Motion, vanilla CSS, or the repo's existing stack.

Do not assume access to paid MotionSites prompts. Learn from the structure and visible examples only.

## Reference Transformation Template

Use this when summarizing inspiration:

```text
Reference pattern:
- Source: [Mobbin category / public site / generated route]
- Useful logic: [hierarchy, motion, layout, state, density]
- Risk: [too common, too heavy, too close to source, poor mobile fit]
- Transformation: [how to adapt into a fresh design for this product]
```

## Guardrails

- Do not copy protected brand assets, paid prompt text, exact layouts, or proprietary screenshots into deliverables.
- Do not let inspiration delay execution. Reference gathering should usually take minutes, not become a research project.
- Prefer evidence from real shipped products for UX flows and generated imagery for mood exploration.
- When a brand or locale is specified, keep output in the brand's language and regional voice unless the user asks otherwise.
