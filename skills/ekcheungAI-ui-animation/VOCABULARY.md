# Animation Vocabulary (reverse-lookup)

Turn a vague description of a motion effect into the precise term, so Elvin knows what to ask for. Load this in Name-effect mode. Adapted from Emil Kowalski's animation-vocabulary (MIT).

## How to answer

1. **Read for intent, not keywords** — users describe what they *see/feel* ("springy", "slides off", "draws itself in"), not the technical name. Map the sensation to the glossary.
2. **Lead with the term**, one-line definition. If several fit, list the best first, then 1–2 alternates with how they differ.
3. **Disambiguate close pairs** (Clip-path vs Mask, Pop in vs Bounce, Shared-element vs Layout).
4. If nothing matches exactly, name the closest and say it's an approximation. Keep it tight — a naming question wants a name, not an essay.

Format:
```
**Stagger** — Animate several items one after another with a small delay between each, creating a cascade.
```

## Glossary

### Entrances & exits
- **Fade in / out** — appear/disappear by changing opacity.
- **Slide in** — enters by sliding from off-screen (a side).
- **Scale in** — grows from smaller to full size, often paired with a fade.
- **Pop in** — appears with a slight overshoot, bounces into place.
- **Reveal** — uncovered gradually via clip-path or mask.
- **Enter / Exit** — the animation played when an element is added to / removed from the screen.

### Sequencing & timing
- **Keyframes** — defined points (0/50/100%) the browser fills between.
- **Interpolation / Tween** — generating the in-between frames so motion is continuous.
- **Stagger** — several items animate one after another with a small delay; a cascade.
- **Orchestration** — deliberately timing multiple animations so they feel like one motion.
- **Delay / Duration** — time before an animation starts / how long it takes.
- **Fill mode** — whether an element keeps its first or last frame's styles before/after (e.g. `forwards`).
- **Stepped animation** — divided into discrete steps, like a countdown.

### Movement & transforms
- **Translate / Scale / Rotate / Skew** — move / resize / spin / slant.
- **3D tilt / Flip** — rotate in 3D (rotateX/Y) for depth.
- **Perspective** — how strong the 3D depth looks.
- **Transform origin** — the anchor point a scale/rotation grows or spins from.
- **Origin-aware animation** — element animates out of its trigger (a popover growing from the button that opened it) instead of from its own center.

### Transitions between states
- **Crossfade** — one element fades out as another fades in, same spot.
- **Continuity transition** — a change that keeps you oriented by visually connecting before and after.
- **Morph** — one shape smoothly turns into another (Dynamic Island).
- **Shared element transition** — an element travels and transforms from one position/screen into another.
- **Layout animation** — an element smoothly animates to a new size/position when layout changes.

### Physics & feel
- **Spring** — motion driven by simulated physics; settles rather than running a fixed duration.
- **Bounce / Overshoot** — passes the target then settles back.
- **Rubber-banding** — resistance and snap-back when dragging past a boundary (iOS overscroll).
- **Momentum / Inertia** — keeps moving after release, decelerating.
- **Magnetic** — an element is pulled toward the cursor as it approaches.

### Surface / decorative
- **Shimmer / Shine** — a highlight sweeps across a surface.
- **Parallax** — layers move at different speeds to imply depth.
- **Marquee** — content scrolls continuously in a loop (linear easing).
- **Draw-on** — a stroke/path appears as if being drawn (SVG `stroke-dashoffset`).

## Disambiguation notes
- **Pop in vs Bounce** — Pop in = single subtle overshoot on entrance; Bounce = repeated oscillation (usually too much for UI).
- **Morph vs Crossfade vs Shared-element** — Morph = shape→shape in place; Crossfade = fade over each other in place; Shared-element = travels *and* transforms across positions.
- **Clip-path vs Mask (for Reveal)** — clip-path clips to a geometric shape; mask uses an image/gradient's alpha (softer edges).
- **Layout animation vs Shared-element** — Layout = same element, new size/position; Shared-element = conceptually the same thing represented by different nodes across views.
