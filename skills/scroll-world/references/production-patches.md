# Production patches + site-integration pattern

Two engine patches and one integration pattern earned shipping a continuous-forward-take
scroll world (Architecture A) on a real, mobile-heavy marketing site. They apply to any
project using the engine, not one brand.

## Patch 1 — iOS decoder-slot release (`unloadClip`)

**Symptom:** on iOS Safari, scenes go blank from the 3rd–4th clip onward even though desktop
is perfect. Root cause: iOS keeps only roughly **three media elements decodable at once**; a
fourth blob-backed `<video>` silently renders blank — no error, no event.

**Fix (in `scrub-engine.js`):** on phones, release a clip once the camera is well past it —
revoke the blob URL, strip `src`, `load()`, remove the element, clear `hasClip/ready/cur`, and
let the still poster take over. The clip reloads on approach. Hysteresis prevents thrash:
**load within 1.6 vh, unload beyond 2.5 vh** of the segment. A per-section **generation
token** (`s.gen`) is bumped on unload so an in-flight blob fetch that resolves late gets
discarded instead of resurrecting a released video.

```
loadClip():   const gen = s.gen = (s.gen || 0);
              …after fetch: if (s.gen !== gen) return;   // unloaded mid-flight
update():     else if (isMobile() && (s.hasClip || s.loading) &&
                 (y < s.start - 2.5*vh || y > s.end + 2.5*vh)) unloadClip(s);
```

Porting rule: never keep more than ~3 live video elements on iOS; poster-first +
reload-on-approach is the pattern.

## Patch 2 — final-scene hold

**Symptom:** after the last scene's scroll segment ends, the world computes the final scene as
"outside" and fades it, dissolving to empty sky just as a content section below the world
slides up.

**Fix:** the last segment's `outside` distance is forced to 0 once `y > s.end`, so the finale's
last frame stays painted under the incoming content section:

```
if (y < s.start) outside = s.start - y;
else if (y > s.end) outside = (i === NSEG - 1) ? 0 : y - s.end;
```

## Pattern — world ↔ normal-site coexistence

To put the world at the top of an otherwise-normal page (nav + real content below):

- Mount the engine with `nav: false` — the site's own nav is the nav.
- Measure the engine's `.sw-track` height, and on scroll toggle two body classes:
  - `in-world` (while `y < trackHeight - navH`): the site nav becomes a transparent overlay
    floating on the flight.
  - `world-done` (past the world): world layers hidden, nav returns to its solid sticky look,
    normal page content takes over.
- Re-measure on `resize`, `orientationchange`, and `load`. The two body-state styles live in
  the site stylesheet, not the engine.

Minimal shape (vanilla; adapt to any framework):

```js
const container = document.getElementById('world');
mountScrollWorld(container, { nav: false, /* sections, connectors, pacing … */ });

const body = document.body;
let worldEnd = 0;
const measure = () => { const t = container.querySelector('.sw-track'); worldEnd = t ? t.offsetHeight : 0; };
const update  = () => {
  const y = window.scrollY || 0, navH = 72;
  const inWorld = worldEnd > 0 && y < worldEnd - navH;
  body.classList.toggle('in-world', inWorld);
  body.classList.toggle('world-done', !inWorld);
};
measure(); update();
addEventListener('scroll', update, { passive: true });
addEventListener('resize', () => { measure(); update(); });
addEventListener('orientationchange', () => { measure(); update(); });
addEventListener('load', () => { measure(); update(); });
```

## Asset + encode conventions that held up

- Stills double as `<video>` posters and reduced-motion fallbacks — keep them.
- Ship both a desktop master (native res, crf 20, `-g 8`, faststart, no audio) and a lighter
  mobile sibling (720p, `-g 4`, crf 23) per clip when the audience is mobile-heavy.
- One video model for the whole chain; each leg's `--start-image` is the previous leg's actual
  extracted last frame; no `--end-image` on legs (Architecture A).
- Cache-bust asset URLs (`?v=N`) and bump on every regeneration — a stale-CDN still looks like
  a seam pop but isn't.

## QA that caught real bugs

- iOS Safari on a real phone, scroll the whole journey twice (down + up) — the only reliable
  repro for the decoder-slot blanking; desktop Safari won't show it.
- Scroll past the world's end and back — the finale frame must stay under the content section
  (Patch 2 regression check).
