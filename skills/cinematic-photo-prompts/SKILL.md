---
name: cinematic-photo-prompts
description: Write cinematic iPhone-style documentary photo prompts for a subject character that feel like real founder video stills — not AI-generated portraits. Use when generating social photo assets, character stills, carousel frames, Reels source frames, or any image that must look like it was shot by another person during a real conversation or founder moment. Covers shot archetypes, lens/camera recipes, blocking, lighting, color grade, and negative prompts for non-AI-feeling photorealism.
---

# Cinematic Photo Prompts

## Core Principle

**Do not prompt for a portrait. Prompt for a camera operator observing a real interaction.**

Every generated frame must pass the "another person is present" test. The viewer should believe someone else is holding the camera, filming or photographing the subject during a real moment — not that the subject posed for a headshot.

## The Non-AI Feeling Checklist

These are the techniques that separate a photorealistic documentary still from an AI-generated portrait. Apply all of them to every prompt:

| Technique | What to do | What to avoid |
|---|---|---|
| **Conversation proof** | Include a foreground listener shoulder, back of head, microphone arm, laptop edge, or opposite chair | Subject staring directly into camera with nothing in foreground |
| **Subject behavior** | The subject is speaking, listening, thinking, looking toward someone, or caught mid-work | The subject posing, smiling at camera, or standing still for a headshot |
| **Camera imperfection** | Specify handheld softness, slight motion, sensor noise, realistic optical depth | Over-sharp AI skin, studio-perfect lighting, glossy stock-photo polish |
| **Lighting source** | Name a real light source: window, practical lamp, spotlight, city bokeh, monitor glow | Generic "soft studio lighting" with no physical source |
| **Props and specificity** | Microphone stands, drinks, laptops, notebooks, cables, desk clutter | Empty sterile backgrounds with no real-world objects |
| **Color grade** | Muted warm-neutral, soft contrast, slightly underexposed, controlled highlights | Vibrant, HDR, over-saturated, or fashion-ad color |
| **Negative space** | Leave clean area for post-production text overlay | Baking captions, text, or brand copy into the generated image |
| **Subject size** | The subject is medium or small in frame; environment is visible | Tight headshot crop with no context |

## Shot Archetypes

Choose one archetype per prompt. Read `references/shot-taxonomy.md` for full camera recipes.

| Archetype | Best for | Lens | Key blocking |
|---|---|---|---|
| `distant_interview_room` | Interviewer signal, coaching, trust | 24–28mm | Listener silhouette across room; subject on lower third |
| `over_shoulder_founder_table` | Strategy, consulting, product walkthroughs | 28–35mm | Foreground shoulder/laptop; subject across table |
| `workspace_turnback` | Students, building, coding, "caught mid-work" | 28–35mm | Desk/monitors behind; subject turning back toward speaker |
| `side_profile_listening` | Premium mood, reflection, confidence | 50–77mm | Profile sharp; background bokeh; foreground glass/plant |
| `rear_silhouette_window` | Freedom, leverage, founder reflection | 35–50mm | Rear silhouette at window; city bokeh beyond glass |
| `sunlit_chair_direct` | Direct hook frame, clean overlay space | 35–50mm | Hard window shadows; large blank wall for copy |
| `lifestyle_two_shot` | Social proof, offline relationships, lifestyle | 28–35mm | Two people mid-conversation; car/table/door creates depth |
| `monochrome_work_desk` | Deep work, focus, process | 28–35mm | B&W, laptop/desk, dark background |
| `architectural_corridor_walk` | Premium movement, authority | 24–35mm | Full-body walk, bright corridor, shadows |
| `tiny_chair_blank_wall` | Text-overlay-first frames | 24–35mm | Tiny subject, huge white wall, minimal props |
| `side_writing_table` | Thinking, planning, reflection | 35–50mm | Writing by hand, window light, books |
| `team_workshop_discussion` | Social proof, collaboration | 28–35mm | Standing speaker, others blurred, B&W |
| `audience_view_keynote` | Teaching, authority, scale | 50–77mm | Crowd foreground, speaker distant |
| `stage_spotlight_speaker` | Premium authority, event | 50–77mm | Dark stage, spotlight, mic, gesture |
| `doorframe_event_speaker` | Candid event documentation | 35–50mm | Shot through door/gap, audience depth |
| `panel_lounge_speaker` | Thought leadership, panel | 35–50mm | Seated with mic, lounge chair, screen behind |

## Base Prompt Structure

Use this skeleton for every generation. Fill in the bracketed sections.

```text
Create a [high-quality realistic / candid iPhone documentary] photo still using the attached subject face references as the identity lock.

FORMAT:
[Native 16:9 / 4:5 / 9:16] composition for [surface]. Raw photo/video-frame reference only. No text, no captions, no logo, no UI overlay, no watermark. Leave clean negative space [location] for later social text overlay.

IDENTITY:
Keep the same subject identity across every frame, driven by the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt). Repeat those traits in every prompt and preserve facial proportions and hairline across angles. Do not make the subject older, more muscular, celebrity-like, stylized into a mascot, or over-glamourized.

SCENE:
[Describe the real situation: who the subject is speaking/listening to, the location, props, and what the viewer should understand about the moment.]

CAMERA:
Shot by another person on an iPhone 15 Pro / iPhone 16 Pro [ProRes documentary video still / as a candid photo]. Lens [24mm / 28mm / 35mm / 50mm / 77mm] equivalent. Camera height: [seated eye level / chest height / standing eye level / slightly high / slightly low]. Angle: [over-the-shoulder / side profile / distant interview room / rear silhouette / handheld lifestyle]. Subject size: [wide / medium-wide / medium close-up]. The subject is [on left third / right third / lower left / center background], looking [toward the listener / off-camera / down at laptop / out window], with [small hand gesture / listening posture / relaxed hands]. [Foreground blocking description]. Do not let the foreground object cover the subject's face.

LIGHT / QUALITY:
High-quality social video still, [light source description], muted warm-neutral color grade, soft contrast, realistic shadows, subtle handheld imperfection, gentle sensor noise, real skin texture, premium founder/operator documentary feel. Not a glossy stock photo, not a studio headshot, not an AI portrait.

NEGATIVE:
No readable text, no generated captions, no fake text glyphs, no UI words, no logos, no watermarks, no poster typography, no QR code, no product ad layout, no over-sharpened HDR, no plastic skin, no waxy face, no celebrity glamour. Do not change identity, do not add facial hair, glasses, hats, earrings, heavy makeup, tattoos, suit styling, exaggerated jawline, distorted eyes, cropped head, extra fingers, warped hands, inconsistent hairline, or duplicate the subject.
```

## Universal Quality Lock

Add this to every prompt's LIGHT / QUALITY block:

```text
High-quality social video still, shot by another person on iPhone 15 Pro / iPhone 16 Pro ProRes or a compact mirrorless documentary camera, natural handheld framing, realistic optical depth, subtle lens softness, real skin texture, gentle sensor noise, muted warm-neutral color grade, soft contrast, controlled highlights, believable shadows. Premium founder/operator documentary feel, not a glossy stock photo, not a studio headshot, not an AI portrait.
```

## Lighting Archetypes (from reference study)

The validated reference images use several distinct lighting approaches:

**Dark studio spotlight** — Near-black background, single key light pool on subject(s), strong vignette. Used for podcast/interview stills. Prompt: `dark studio, single overhead spotlight, near-black background, strong vignette, controlled key light on face and upper body`.

**Hard window side light** — Architectural window creates geometric shadows on wall and floor. Most natural-looking. Prompt: `hard window sunlight from [left/right], geometric rectangular shadows on wall and floor, soft ambient fill, realistic highlight rolloff`.

**Warm practical indoor** — Real room lamps, pendant lights, or warm ambient. Used for cafe/coworking lifestyle shots. Prompt: `warm indoor practical light, pendant lights, soft ambient fill, warm-neutral grade, real room atmosphere`.

**B&W high contrast** — Film-grain black and white conversion. Strongest "not AI" signal. Prompt: `black and white documentary still, high contrast, strong film grain, deep shadows, controlled highlights, no color`.

**Warm event/stage light** — Warm practicals, track lights, or stage spots. Used for speaking scenes. Prompt: `warm indoor event track lights, soft stage spot, realistic audience depth`.

**Architectural corridor daylight** — Bright neutral concrete, clean and premium. Prompt: `soft daylight, pale neutral concrete, bright window side, low-saturation editorial cleanliness`.

**Through-glass reflection** — Adds layered depth and documentary authenticity. Prompt: `shot through glass, realistic window reflections, layered depth`.

## Reference Selection for Generation

Provide your own subject's face-reference images as input to the image model for consistency. Use 3–4 references per generation call:

- **Identity lock:** front neutral + one three-quarter + one profile
- **Expanded expression set:** front neutral + front confident + smile + thinking + surprised + side-45 + both profiles
- **Talking-head/avatar:** front neutral + front confident + smile/thinking as needed
- **Social poster cameo:** one front or three-quarter is sufficient

Prepare these references yourself — a small photo set of your subject shot from multiple angles and expressions — and pass the images directly to the image model as reference inputs. No absolute file paths or external reference-sheet skills are required.

## Output Format Defaults

- **16:9** is the default for video stills, Reels frames, YouTube/CapCut source frames, and future crop flexibility
- **4:5** for Instagram feed photo assets
- **9:16** only when the final asset must be vertical-first

## First Batch Protocol

For a first review batch, generate exactly these three archetypes:
1. `distant_interview_room` — strongest conversation/interviewer signal
2. `over_shoulder_founder_table` — consulting/founder strategy
3. `side_profile_listening` — emotional premium mood

Review identity, realism, and camera quality before continuing to other archetypes.

## QA Rubric

**Accept when:**
- The frame reads as shot by another person during a real conversation
- The subject's hair, face shape, wardrobe, and calm operator expression are consistent with references
- The image has premium social-video quality: controlled light, realistic skin, soft contrast, subtle grain
- The composition has usable copy space for later overlays
- No generated text, logos, QR codes, readable UI, or fake glyphs are present

**Revise when:**
- The photo looks like a posed headshot or corporate stock meeting
- The foreground object blocks the subject's face or competes as the main subject
- The subject looks older, muscular, celebrity-like, or over-glamourized versus the references
- The output has plastic skin, warped hands, inconsistent hairline, or multiple lookalike people
- The lighting is generic studio soft-box with no real-world source

## Reference Files

- `references/shot-taxonomy.md` — Full camera/lens recipes for all archetypes with failure modes
- `references/detailed-prompt-recipes.md` — Copy-ready full prompts for all archetypes, validated batch defaults, and QA rubric
