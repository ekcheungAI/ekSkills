# ekcheung.com brandflush — production learnings

Everything here was earned on the ekcheung.com homepage rebuild (branch
`scroll-world-rebrand`, July 2026): 「升級之旅」The Upgrade Journey — vinyl-toy
miniature Hong Kong, light theme, 5 scenes, one continuous forward flight:
城市 → 返工 → 茶餐廳 → 屋邨 → 你間房部電腦.

## The build in one config

See `world-init-example.js` for the full live config. Key choices:

- Architecture A (continuous forward take), `connectors: []`, `crossfade: 0.08`.
- `nav: false`, `atmosphere: true`, `diveScroll: 1.15`, `hint: '向下滾動'`.
- Per-scene pacing: scene 1 `scroll:1.5, linger:0.3`; scene 3 `scroll:1.2`;
  finale `scroll:1.8, linger:0.45` (holds while the CTA copy peaks).
- Finale carries the CTA: primary → `#content-entry` (the content sheet below the
  world), secondary → YouTube subscribe URL.
- Palette: brand blue `#075BFF`; yellow family darkened to `#C88A00` for text
  contrast on the light background.
- Asset URLs cache-busted (`?v=4` on stills, `?v=1` on clips) — bump on every
  regeneration or the CDN serves stale frames.

## Site patch 1 — iOS decoder-slot release (`unloadClip`)

**Symptom:** on iOS Safari, scenes went blank from the 3rd–4th clip onward even
though desktop was perfect. Root cause: iOS keeps only roughly **three media
elements decodable at once**; a fourth blob-backed `<video>` silently renders
blank — no error, no event.

**Fix (in `scrub-engine.js`):** on phones, release a clip once the camera is well
past it — revoke the blob URL, strip `src`, `load()`, remove the element, clear
`hasClip/ready/cur`, and let the still poster take over. The clip reloads on
approach. Hysteresis prevents thrash: **load within 1.6 vh, unload beyond 2.5 vh**
of the segment. A per-section **generation token** (`s.gen`) is bumped on unload so
an in-flight blob fetch that resolves late gets discarded instead of resurrecting a
released video.

```
loadClip():   const gen = s.gen = (s.gen || 0);
              …after fetch: if (s.gen !== gen) return;   // unloaded mid-flight
update():     else if (isMobile() && (s.hasClip || s.loading) &&
                 (y < s.start - 2.5*vh || y > s.end + 2.5*vh)) unloadClip(s);
```

If porting the engine anywhere: never keep more than ~3 live video elements on
iOS; poster-first + reload-on-approach is the pattern.

## Site patch 2 — final-scene hold

**Symptom:** after the last scene's scroll segment ended, the world computed the
final scene as "outside" and faded it, dissolving to empty sky just as the content
sheet slid up.

**Fix:** the last segment's `outside` distance is forced to 0 once `y > s.end`,
so the finale's last frame stays painted under the incoming content sheet:

```
if (y < s.start) outside = s.start - y;
else if (y > s.end) outside = (i === NSEG - 1) ? 0 : y - s.end;
```

## Site-nav coordination (world ↔ real site)

The engine renders no nav (`nav: false`). `world-init.js` measures `.sw-track`
height and on scroll toggles:

- `body.in-world` — while inside the world: the site nav becomes a transparent
  overlay floating on the flight.
- `body.world-done` — past the world: world layers hidden, nav returns to its
  sticky solid look, normal page content (the "content sheet") takes over.

Threshold: `y < trackHeight - navH` (navH 72). Re-measure on `resize`,
`orientationchange`, and `load`. CSS for the two body states lives in the site
stylesheet, not the engine.

## Asset + encode conventions

- Stills: `/images/world/scene-0N.webp` — double as posters and reduced-motion
  fallbacks.
- Clips: `/videos/world/scene-0N.mp4` (1080p, crf 20, `-g 8`, faststart, no audio)
  and `scene-0N-m.mp4` (720p, `-g 4`, crf 23) — always ship both for ekcheung.com.
- One model for the whole chain (`seedance_2_0`); each leg's `--start-image` is the
  previous leg's actual extracted last frame; no `--end-image` on legs.

## QA that caught real bugs

- iOS Safari on a real phone, scroll the entire journey twice (down + up) — this is
  the only reliable repro for the decoder-slot blanking; desktop Safari won't show it.
- Scroll past the world's end and back — the finale frame must stay under the
  content sheet (patch 2 regression check).
- After regenerating any asset, verify the `?v=` bump actually reached the HTML —
  stale-CDN stills look like a seam pop but aren't.
