---
name: website-design
description: Contemporary website and web-app design direction for landing pages, marketing sites, portfolios, SaaS dashboards, product pages, and frontend UI reviews. Use when the agent needs to design, build, restyle, critique, or art-direct a modern web experience; choose current visual systems, section rhythm, hero composition, typography, color/material treatment, motion, responsive behavior, and anti-generic checks. Triggers include requests for trending website design, premium UI, Awwwards-style direction, MotionSites-style hero prompts, imagegen inspiration, Mobbin app/web references, conversion-focused landing pages, modern SaaS websites, website redesigns, design-system direction, UI polish, visual QA, and avoiding AI-looking web layouts.
---

# Website Design

## Operating Mode

Create web experiences that feel current, specific, usable, and implementation-ready. Treat trends as tools, not decoration. Every design choice must serve the product, audience, content hierarchy, conversion path, or interaction clarity.

Default to high craft:

- Strong first-viewport concept, not a generic centered hero.
- Typography as a primary design material.
- Images, product visuals, or tactile media as structural elements when the brief allows.
- One coherent design system across the full page.
- Responsive, accessible, fast, and shippable implementation.

## Workflow

1. Parse the brief: audience, product category, conversion goal, brand maturity, content density, stack, and constraints.
2. Choose the register:
   - `brand`: marketing, landing, creator, campaign, portfolio, editorial, and product-story pages where design carries identity and persuasion.
   - `product`: SaaS tools, dashboards, admin panels, workflow surfaces, settings, forms, onboarding, and data-heavy UI where design serves repeated use.
3. Gather references before designing when the task is open-ended: use Mobbin MCP for real app/product patterns when available, current web sources for public landing-page trends, and imagegen for 2-4 quick visual exploration comps when the user wants inspiration or a strong visual direction.
4. Choose a design thesis in one sentence: the visual world, emotional tone, and interaction promise.
5. Set design dials: visual ambition, information density, image reliance, motion level, conversion discipline, implementation clarity, and brand fidelity.
6. Select a pattern stack: hero architecture, section rhythm, typography character, palette/material system, component language, and motion behavior.
7. Apply the relevant review mode when the user asks for a specific kind of work: `shape`, `critique`, `polish`, `harden`, `typeset`, `layout`, `adapt`, or `clarify`.
8. Implement or describe the design with concrete decisions: layout, spacing, type scale, images, states, responsive behavior, and accessibility.
9. Run the deterministic anti-pattern pass and QA checklist before completion. If building code, verify in browser at desktop and mobile widths.

## Load References

- Read `references/trend-intelligence-2026.md` when the user asks for trending/current/modern design, or when choosing a direction from scratch.
- Read `references/inspiration-research.md` when using Mobbin MCP, imagegen, MotionSites/Viktor Oddy-style prompt inspiration, or any external visual references.
- Read `references/art-direction-matrix.md` when designing a page, hero, landing page, visual concept, or image-generation prompt.
- Read `references/qa-checklist.md` before claiming a design, frontend implementation, or UI review is complete.

## Design Rules

- Avoid default AI web patterns: purple-blue glow gradients, floating blobs, generic dashboard cards, repeated centered sections, weak startup copy, and cloned text-left/image-right blocks.
- Do not make every section a card. Use full-width bands, editorial compositions, image-led sections, restrained bento grids, and negative space.
- Use bento grids only when the content benefits from modular hierarchy. Vary card size and keep whitespace generous.
- Use glass, translucency, gradients, 3D, and scroll motion only with a clear purpose. They must improve hierarchy, comprehension, product inspection, or narrative flow.
- Treat references as ingredients, not templates to clone. Extract pattern logic, spacing, motion, hierarchy, and content strategy; create a new direction for the user's product.
- Prefer purposeful asymmetry over decorative chaos. Broken grids still need scan order.
- Keep one palette, one type system, one radius language, one shadow/elevation logic, and one icon style across the page.
- Make the primary action obvious. Vary CTA styling only when it supports section role and conversion hierarchy.
- Keep body text readable, buttons stable, mobile layout first-class, and touch targets large enough.
- For `brand` register, allow stronger typography, imagery, asymmetry, motion, and campaign-like rhythm when they improve identity or conversion.
- For `product` register, reduce visual ambition before reducing usability: prioritize dense scanning, predictable controls, stable states, semantic color, and fast repeated action.
- Treat outside design skills as review mechanics, not brand overrides. Do not replace project-specific typography, palette, language/tone, or visual assets just because an external skill bans a pattern globally.

## Review Modes

- `shape`: define register, design thesis, dials, user flow, section/component structure, and acceptance criteria before implementation.
- `critique`: find hierarchy, clarity, UX, accessibility, brand-fit, and anti-pattern issues before suggesting fixes.
- `polish`: tighten spacing, type scale, contrast, component consistency, copy, states, responsive behavior, and final visual rhythm.
- `harden`: add or review loading, empty, error, disabled, focus, long-text, i18n, mobile, reduced-motion, and performance states.
- `typeset`: fix font pairing, heading/body scale, line length, label density, button text fit, and multilingual/CJK readability.
- `layout`: fix grid, spacing rhythm, scan order, media framing, card overuse, responsive collapse, and overlap.
- `adapt`: adjust a design for device, density, audience, brand/product register, or implementation constraints.
- `clarify`: rewrite UX copy, labels, CTAs, error messages, empty states, and AI capability explanations into specific, believable language.

## Output Expectations

When planning or reviewing, return:

- Design thesis
- Register and design dials
- Inspiration sources used
- Pattern stack
- Section-by-section direction
- Anti-pattern risks
- Implementation notes
- QA risks

When coding, edit the existing project patterns first, then verify with the most relevant local checks and browser viewports.
