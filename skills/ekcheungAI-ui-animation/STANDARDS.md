# Animation Standards (precise catalog)

The exact values behind the review. Cite these instead of approximating. Adapted from Emil Kowalski's design engineering standards (MIT), tuned to the ekOS/HeyOmmi stack. Load this in Audit, Review, and Build-new modes.

## Should it animate? (frequency gate)

| Frequency | Decision |
| --- | --- |
| 100+/day (keyboard shortcuts, command palette toggle, core nav) | **No animation. Ever.** |
| Tens/day (hover, list nav, frequent toggles) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, feedback, celebration) | Can add delight |

**Never animate keyboard-initiated actions** — repeated hundreds of times daily; motion makes them feel slow and disconnected. Valid purposes for motion: spatial consistency, state indication, explanation, feedback, preventing a jarring change. "It looks cool" on a frequently-seen element is not valid.

## Easing

Decision order:
- Entering / exiting → **ease-out** (starts fast, feels responsive)
- Moving / morphing on screen → **ease-in-out**
- Hover / color change → **ease**
- Constant motion (marquee, progress) → **linear**
- Default → **ease-out**

**Never `ease-in` on UI.** It starts slow, delaying the exact moment the user is watching. `ease-out` at 200ms *feels* faster than `ease-in` at 200ms.

Built-in CSS easings are too weak. Use strong curves. **In ekOS these are tokens — use the token, do not hand-roll a one-off `cubic-bezier`:**

```css
/* Defined in HeyOmmi app/globals.css @theme inline → generate ease-*-strong utilities */
--ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);      /* UI enter / press feedback */
--ease-in-out-strong: cubic-bezier(0.77, 0, 0.175, 1);  /* on-screen movement / morph */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);          /* iOS-like drawer / sheet */
```

Tailwind usage: `ease-out-strong`, `ease-in-out-strong`, `ease-drawer`. Raw CSS: `transition-timing-function: var(--ease-out-strong)`. In a project without these tokens, add them to the theme first (or use the raw curves above), rather than scattering magic numbers. Find new curves at [easing.dev](https://easing.dev/), don't invent from scratch.

## Duration

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing / explanatory | can be longer |

**Rule: UI animations stay under 300ms.** A 180ms dropdown feels more responsive than a 400ms one. Faster spinners make load *feel* faster. Skip the tooltip delay after the first (instant on repeat) so a toolbar feels fast.

## Physicality

- **Never `scale(0)`.** Start from `scale(0.9–0.97)` + `opacity: 0`. Nothing in the real world appears from nothing.
- **Origin-aware popovers.** Scale from the trigger, not center:
  - Radix (HeyOmmi): `origin-(--radix-popover-content-transform-origin)` / `--radix-dropdown-menu-content-transform-origin` / `--radix-select-content-transform-origin` / `--radix-tooltip-content-transform-origin`
  - Base UI: `transform-origin: var(--transform-origin)`
  - **Modals are exempt** — centered in viewport, keep `transform-origin: center`.
- **Button press feedback.** `active:scale-[0.97]` (subtle 0.95–0.98) on any pressable element, `transition-transform` ~150ms ease-out-strong.

## Interruptibility

CSS **transitions** can be retargeted mid-animation; **keyframes** restart from zero. For anything triggered rapidly (toasts added, toggles, list add/remove) transitions are smoother.

```css
.toast { transition: transform 300ms var(--ease-out-strong); }        /* interruptible — good */
@keyframes slideIn { from { transform: translateY(100%);} to {…} }     /* restarts — avoid for dynamic UI */
```

Use `@starting-style` for entrance without JS. Percentages (`translateY(100%)`), not hardcoded px, so exits mirror entrances.

## Springs (JS / Motion only)

No fixed duration — settle on parameters. Use for: drag with momentum, "alive" elements, interruptible gestures. Springs keep velocity when interrupted (keyframes restart), so they win for gestures a user may reverse.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }   // Apple-style — recommended
```

Keep bounce subtle (0.1–0.3); avoid bounce in most UI — reserve for drag-to-dismiss / playful. Mouse-tracking: interpolate with `useSpring`, only when the motion is decorative.

## Accessibility

Every custom animation must be neutralized under `prefers-reduced-motion: reduce`. HeyOmmi's `globals.css` opens that block with a **universal catch-all** (`*` → near-zero durations) plus explicit `animation: none` on named classes — extend that block for new keyframes; never ship motion that bypasses it.

## Audit severity (for Audit mode reports)

- **HIGH** = feel-breaking: animation on keyboard/100+/day actions · `ease-in` on UI · dropped frames · `scale(0)` · `transition: all` on hot paths.
- **MEDIUM** = noticeably off: wrong transform-origin · non-interruptible dynamic UI · missing reduced-motion · > 300ms on interactive UI.
- **LOW** = polish: stagger, token consolidation, blur-masked crossfades.

Order findings by leverage (impact ÷ effort). Fix at shared primitives before call sites.
