---
name: scroll-world
description: >
  Build a scroll-scrubbed "fly through the world" cinematic landing page. As the visitor
  scrolls, a pre-rendered camera flight moves through connected scenes with no cuts; scroll
  only scrubs time (the same technique behind Apple's scroll-through product pages). Use when
  you want a scroll world, scroll cinematic, diorama/miniature-world hero, "fly-through"
  landing, or need to fix mobile/iOS scrub issues (blank scenes, frozen video, seam pops).
  This is an adaptation of the scroll-world plugin v0.1.3 (MIT, © 2026 cyw — see LICENSE)
  with two production patches earned shipping it on a real site.
---

# scroll-world

Produces a landing page where **scroll drives a camera**: it flies through pre-rendered,
seamlessly-connected scenes as the visitor scrolls. The visuals are AI-generated (Higgsfield);
the page just scrubs pre-rendered video by scroll position. The camera genuinely moves —
scroll only drives time.

This skill adds two things to the upstream plugin:

1. **A patched scrub engine** (`references/scrub-engine.js`) — carries production fixes for
   iOS media-decoder limits and end-of-journey handling that the stock engine lacks.
2. **A production-patches writeup** (`references/production-patches.md`) — the engineering
   lessons + a framework-agnostic pattern for making the world coexist with a normal site
   (nav coordination, a content section below the world).

## Full pipeline

The complete generation pipeline (interview → scene stills → camera clips → seamless chain →
encode → assemble → seam QA) is in `references/upstream-skill.md` — follow it as written; it
is the methodology. Prompt templates in `references/prompts.md`, batch scripts in
`references/pipeline.md`, background knockout in `references/knockout.py`, a minimal standalone
page in `references/index-template.html`.

Sensible defaults:

- **Architecture A (continuous forward take)** with `connectors: []` — the legs ARE the
  journey; every seam is frame-identical and the camera never reverses.
- Video model `seedance_2_0`; stills `gpt_image_2`; encode per the upstream Step 6 (native
  res, crf 20, `-g 8`, faststart; mobile siblings 720p `-g 4`).
- Always ship the `-m.mp4` mobile encodes if any meaningful share of the audience is on phones.

## Production patches in the engine (why they exist)

Full detail + the exact diffs are in `references/production-patches.md`:

- **iOS decoder-slot release (`unloadClip`)** — iOS Safari only keeps ~3 media elements
  decodable at once; a 4th blob video renders blank. On phones the engine releases clips once
  the camera is well past them (hysteresis: load within 1.6 vh, unload beyond 2.5 vh) so the
  active scene always gets a decoder slot. A generation token discards in-flight loads. Fixes
  "blank scenes after the 3rd clip" on iOS.
- **Final-scene hold** — the last scene's final frame is held after its segment ends, so a
  content section can slide over the world instead of the page dissolving to empty sky.

## Site-integration pattern

`references/production-patches.md` describes a framework-agnostic pattern for embedding the
world at the top of an otherwise-normal page: mount with `nav: false`, then toggle a body
class from scroll position vs the engine's `.sw-track` height so the site nav floats
transparently over the world and returns to its solid sticky state once the world is done.

## Rules

- QA the seams (upstream Step 8) before claiming done — local preview, console clean,
  `video.seekable.end(0) > 0`, and an iOS check for the blank-scene regression.
- Higgsfield generations run detached (3–8 min each); pass local file paths, never job UUIDs,
  to `--image/--start-image/--end-image`.

## References

- `references/upstream-skill.md` — full upstream pipeline (interview, stills, clips, seams,
  encode, assemble, QA, gotchas)
- `references/scrub-engine.js` — the **patched** portable engine (use this one)
- `references/production-patches.md` — the two production patches + site-integration pattern
- `references/prompts.md`, `references/pipeline.md`, `references/knockout.py`,
  `references/index-template.html` — upstream tooling, unchanged
- `LICENSE` — MIT, © 2026 cyw (the upstream scroll-world plugin this adapts)
