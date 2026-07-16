---
name: ekcheungAI-ui-animation
description: Use when adding, reviewing, auditing, or improving any UI animation, transition, motion, easing, hover/press feedback, entrance/exit, or micro-interaction in a web frontend (CSS, Tailwind, Framer Motion/Motion, shadcn/Radix) — or when deciding whether an element should animate at all, naming a motion effect, or reaching for an animated component library. Symptoms include transition-all, ease-in on UI, scale(0), sluggish or over-animated UI, missing :active/press states, janky or non-interruptible motion, and choosing a duration or easing curve.
---

# ekcheungAI-ui-animation

Elvin's animation craft skill: **taste + parts.** It fuses Emil Kowalski's design-engineering standards (the judgment) with animate-ui as a component source (the parts), tuned to the ekOS stack. Default target is HeyOmmi (Next 15/16 · React 19 · Tailwind v4 CSS-first · shadcn `new-york` · `radix-ui`), but the standards are stack-agnostic.

## The one rule that matters most

**Most agents already know the craft (ease-out, no `scale(0)`, specific transitions). What they miss is restraint.** Before touching easing or duration, decide whether the thing should animate *at all*. Over-animating a frequent or keyboard-driven action is the #1 mistake — worse than any wrong curve.

> The premise is Emil's ["You Don't Need Animations"](https://emilkowal.ski/ui/you-dont-need-animations): sometimes the best animation is none.

## Step 0 — The Gate (run this FIRST, every time)

Every candidate animation must survive all four, in order. Record the answers.

**1. Frequency — how often will a user see it?**

| Frequency | Verdict |
| --- | --- |
| 100+/day (keyboard shortcuts, command palette, core nav) | **Reject. No animation. Ever.** |
| Tens/day (hover, list nav, frequent toggles) | Reject, or near-imperceptible only |
| Occasional (modals, drawers, toasts, settings) | Eligible — standard animation |
| Rare / first-time (onboarding, empty/success states) | Eligible — the delight budget lives here |

Keyboard-initiated actions are a **disqualifier, not a judgment call** (Raycast's command palette has no open/close animation — that is correct).

**2. Purpose — name it in one word:** Feedback · Spatial-consistency · State-indication · Preventing-jarring-change · Explanation · Delight (Rare tier only). "It looks cool" is not on the list → reject.

**3. Speed — fits the budget?** UI stays < 300ms (see STANDARDS.md). If it only works as a slow, showy thing → reject.

**4. Function — does motion help or hinder here?** Data the user is reading/acting on must not move for style. Decoration belongs on marketing surfaces, not dense functional UI.

## Modes

Pick by what's being asked. Load the referenced file only when you enter that mode.

| Mode | Trigger | What to do |
| --- | --- | --- |
| **Audit** | "audit / improve the motion", "make this feel better" | Sweep code for violations against **STANDARDS.md**. Run the Gate on each animated element. Report a prioritized table (HIGH/MED/LOW), most-leverage first. Read-only — propose, don't blast-edit. |
| **Review** | reviewing a diff / pre-commit | Grade the changed animation code against **STANDARDS.md**. Output the **Before / After / Why** markdown table (required format below). |
| **Build new** | adding a new element/interaction | Gate first (Step 0). If it passes: build **CSS-first** with ekOS tokens (STANDARDS.md). Escalate to **animate-ui / Motion** only when the Escalation test in **ANIMATE-UI.md** says JS is warranted. |
| **Name effect** | "what's it called when…" | Reverse-lookup in **VOCABULARY.md**. Lead with the term. |

### Required review output format

Never use "Before:"/"After:" on separate lines. Always a single table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 150ms var(--ease-out-strong)` | Name properties; avoid `all` |
| `scale(0)` | `scale(0.96); opacity: 0` | Nothing appears from nothing |
| `ease-in` on entrance | `ease-out` (strong curve) | `ease-in` delays the moment you're watching |
| animate a Cmd+K palette | no open/close animation | 100+/day keyboard action — Gate reject |

## Cheat sheet (full detail in STANDARDS.md)

- **Easing:** entrances/exits → **ease-out**; on-screen movement/morph → ease-in-out; hover/color → ease; constant → linear. **Never `ease-in` on UI.** Built-in curves are weak → use ekOS tokens: `--ease-out-strong`, `--ease-in-out-strong`, `--ease-drawer` (defined in HeyOmmi `app/globals.css` `@theme`; the Tailwind utilities are `ease-out-strong` etc.). Never hand-roll a one-off `cubic-bezier` when a token exists.
- **Duration:** press 100–160ms · tooltip 125–200ms · dropdown 150–250ms · modal/drawer 200–500ms. **UI < 300ms.**
- **Physicality:** never `scale(0)` — start `scale(0.9–0.97)` + `opacity:0`. Buttons get `active:scale-[0.97]`. Popovers scale from their trigger (`origin-(--radix-*-content-transform-origin)`), modals stay centered.
- **Interruptibility:** for rapidly-retriggered UI (toasts, toggles, list add/remove) use **CSS transitions** (retarget mid-flight), not `@keyframes` (restart from zero).
- **Accessibility:** every custom animation must be covered by `prefers-reduced-motion` (HeyOmmi uses a universal catch-all in `globals.css` — extend it, don't bypass it).

## HeyOmmi worked example (the pattern to copy)

The shared Button primitive (`components/ui/button.tsx`) is the reference implementation:
`transition-[color,background-color,border-color,box-shadow,transform] duration-150 ease-out-strong active:scale-[0.97]` — targeted properties, tokenized easing, tokenized-tier duration, universal press feedback. Fix motion at the **primitive**, not per-call-site, so it propagates. HeyOmmi's Radix wrappers (`popover/dropdown-menu/select/tooltip`) are already correctly origin-aware — match them.

## Attribution

Standards adapted from **Emil Kowalski's** [skills](https://github.com/emilkowalski/skills) and [animations.dev](https://animations.dev) (MIT). Component catalog from **animate-ui** (`imskyleen/animate-ui`, MIT). This skill re-expresses their guidance tuned to ekOS; credit and depth belong to the originals.
