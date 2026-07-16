# animate-ui — component source & escalation

When the Gate (SKILL.md Step 0) passes AND CSS can't cleanly express the motion, reach for animate-ui. It is a shadcn-CLI **registry** (copy-paste components, MIT), built on **Motion (Framer)**. Load this file only in Build-new mode when considering JS motion.

## Escalation test — do you actually need Motion?

Default to **CSS-first** (transitions, `@starting-style`, the ekOS easing tokens). Escalate to animate-ui / Motion **only** when one of these is true:

1. **Physics / gestures** — drag-to-dismiss, swipe, momentum, interruptible reversal (springs; CSS can't).
2. **Layout / shared-element** — an element moving between positions/containers (`layout` animations).
3. **Animated numbers** — counters/odometers (`counting-number`, `sliding-number`).
4. **Orchestrated sequences** — staggered enter/exit tied to presence (`AnimatePresence`) that `@starting-style` can't cover.

If none apply → do it in CSS. Adding Motion is a **deliberate dependency decision**: HeyOmmi ships **zero JS-motion runtime today**, so introducing `motion` widens the bundle and adds a second animation paradigm. Flag it before installing.

## Install (registry already wired)

HeyOmmi's `components.json` already declares the `@animate-ui` registry, so:

```bash
npx shadcn add @animate-ui/<name>       # e.g. @animate-ui/counting-number
```

This copies the component into the repo (you own/edit it) and pulls `motion` as a dependency. After adding, re-check the component against STANDARDS.md — registry defaults sometimes over-animate (bounce too high, durations too long); tune to the ekOS tokens.

## Component map (what exists, by category)

- **Text:** counting-number, sliding-number, scrolling-number, shimmering, gradient, typing, rolling, morphing, rotating, splitting, highlight.
- **Effects (wrappers):** magnetic, tilt, shine, blur, fade, slide, zoom, particles, image-zoom, auto-height, highlight.
- **Buttons:** ripple, liquid, flip, copy, icon, theme-toggler, github-stars.
- **Radix wrappers (motion-enhanced):** accordion, dialog, alert-dialog, tabs, tooltip, popover, dropdown-menu, hover-card, sheet, sidebar, switch, checkbox, radio-group, progress, toggle, toggle-group, collapsible.
- **Base UI / Headless wrappers:** same primitives for Base UI and Headless UI stacks.
- **Backgrounds:** gradient, stars, gravity-stars, bubble, fireworks, hexagon, hole.
- **Animated icons:** large lucide-style set with motion-on-hover.
- **Primitives:** spring, motion-grid, scroll-progress, slot, cursor, pinned-list.
- **Community:** motion-carousel, notification-list, flip-card, radial-menu/nav, management-bar, user-presence-avatar, share-button.

## Best-fit picks for HeyOmmi (highest value, lowest risk)

| Component | Where | Why it beats CSS |
| --- | --- | --- |
| `counting-number` / `sliding-number` | analytics dashboards (`components/analytics/*`, Recharts) | animated metric counters — genuine JS-only win |
| `magnetic` / `shine` / `tilt` | marketing / hero surfaces only | decorative; Gate allows on low-frequency marketing |
| Radix motion wrappers | only if a specific primitive needs layout/spring motion CSS can't do | otherwise keep the existing CSS-transition shadcn primitives |

**Do NOT** wholesale-swap HeyOmmi's shadcn primitives for animate-ui's — that trades a lean, controlled CSS system for a JS runtime with poor ROI. Cherry-pick per the Escalation test.
