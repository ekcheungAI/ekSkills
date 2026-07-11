---
name: ekcheungai-scroll-world
description: >
  Build or extend a scroll-scrubbed "fly through the world" cinematic landing page for
  ekcheung.com or an @ekcheungAI client brand — the brandflush homepage effect. As the
  visitor scrolls, a pre-rendered Higgsfield camera flight moves through connected scenes
  with no cuts; scroll only scrubs time. Use when the user wants a scroll world, scroll
  cinematic, diorama/miniature-world hero, "fly-through" landing, new scenes for the
  ekcheung.com homepage journey, seam/scrub QA, or fixes for mobile/iOS scrub issues
  (blank scenes, frozen video, seam pops). This is the ekcheungAI-adapted clone of the
  scroll-world plugin v0.1.3 with production patches from the ekcheung.com brandflush
  build — always use THIS skill's patched engine, not the upstream plugin copy.
---

# ekcheungai-scroll-world

Clone of the `scroll-world` plugin v0.1.3 (MIT, © 2026 cyw — LICENSE in this folder)
adapted for @ekcheungAI. Two things distinguish it from upstream:

1. **The patched scrub engine** (`references/scrub-engine.js`) — carries production
   fixes that upstream doesn't have. Never regress to the plugin's copy.
2. **The ekcheung.com brandflush integration pattern** — how the world coexists with a
   real site (nav coordination, content sheet, Cantonese copy, brand palette).

## Canonical live implementation

The source of truth is the ekcheung.com repo (`~/Desktop/ekOS/10_brand/ekcheung.com`,
branch `scroll-world-rebrand`):

- `js/scrub-engine.js` — the patched engine (identical to this skill's reference copy)
- `js/world-init.js` — the mount + site-nav coordination (mirrored as
  `references/world-init-example.js`)
- assets: `/images/world/scene-0N.webp` (stills/posters), `/videos/world/scene-0N.mp4`
  + `scene-0N-m.mp4` (desktop + mobile encodes)

If the repo and this skill's engine ever diverge, the repo wins — re-mirror it here.

## Full pipeline

The complete generation pipeline (interview → scene stills → camera clips → seamless
chain → encode → assemble → seam QA) is in `references/upstream-skill.md`. Follow it
as written; it is the methodology. Prompt templates in `references/prompts.md`, batch
scripts in `references/pipeline.md`, background knockout in `references/knockout.py`.

ekcheungAI defaults on top of it:

- **Architecture A (continuous forward take)** with `connectors: []` — the legs ARE the
  journey. This is what the brandflush homepage ships.
- Video model `seedance_2_0`; stills `gpt_image_2`; encode per upstream Step 6
  (native res, crf 20, `-g 8`, faststart; mobile siblings 720p `-g 4`).
- Always produce the `-m.mp4` mobile encodes for ekcheung.com work — the site's audience
  is mobile-heavy; the mobile beta gate in the upstream interview doesn't apply here.

## Site patches in the engine (why they exist)

Details + exact diffs in `references/ekcheung-brandflush.md`:

- **iOS decoder-slot release (`unloadClip`)** — iOS Safari only keeps ~3 media elements
  decodable; a 4th blob video renders blank. On phones the engine releases clips once
  the camera is well past them (hysteresis: load within 1.6 vh, unload beyond 2.5 vh)
  so the active scene always gets a decoder slot. A generation token discards in-flight
  loads. Fixes "blank scenes after the 3rd clip" on iOS.
- **Final-scene hold** — the last scene's final frame is held after its segment ends,
  so the content sheet slides over the world instead of the page dissolving to empty sky.

## ekcheung.com integration pattern

- Mount with `nav: false` — the site nav is the nav. `world-init.js` toggles
  `body.in-world` (nav = transparent overlay on the world) / `body.world-done`
  (world hidden, sticky nav) from scroll position vs `.sw-track` height.
- Pacing: hero + finale scenes get higher `scroll` + `linger` (e.g. 1.5/0.3 and
  1.8/0.45); transit scenes stay brisk. `crossfade: 0.08` for the one-take chain.
- Cache-bust asset URLs with `?v=N` and bump on regeneration.
- Copy: 廣東話（香港語感），tone via the `ekcheungai-tone-framework` skill; eyebrows
  can stay English caps (THE CITY / THE GRIND …). Palette: brand blue `#075BFF`,
  amber-for-text `#C88A00` (darkened yellow for contrast on light bg).
- Visual world: vinyl-toy miniature Hong Kong, light theme — keep the style preamble
  identical across every scene prompt.

## Rules

- QA the seams (upstream Step 8) before claiming done — local preview, console clean,
  `video.seekable.end(0) > 0`, iOS check for the blank-scene regression.
- ekcheung.com production deploys only via `git push` to `main`, and only with Elvin's
  explicit approval. Never `vercel --prod`.
- Higgsfield generations run detached (3–8 min each); pass local file paths, never job
  UUIDs, to `--image/--start-image/--end-image`.

## References

- `references/upstream-skill.md` — full upstream pipeline (interview, stills, clips,
  seams, encode, assemble, QA, gotchas)
- `references/scrub-engine.js` — **patched** portable engine (use this one)
- `references/world-init-example.js` — the live ekcheung.com mount + nav coordination
- `references/ekcheung-brandflush.md` — production learnings + patch diffs
- `references/prompts.md`, `references/pipeline.md`, `references/knockout.py`,
  `references/index-template.html` — upstream tooling, unchanged
