# Cinematic Founder Photo Shot Taxonomy

Use this reference when choosing camera angles for real-life photo prompts. These are derived from founder-video examples: candid conversation scenes, premium interview spaces, close side profiles, rear silhouettes, workspace turnbacks, and lifestyle two-shots.

## Shared Camera DNA

- The camera is held by another person or placed near another participant.
- The subject should rarely stare straight into camera. Prefer listening, explaining, thinking, or looking toward someone off-frame.
- The frame should feel like a video still: slight softness, natural grain, practical light, real-world compression, not a hyper-sharp studio portrait.
- Good prompts describe distance and blocking, not only lens.
- Text should be absent from the generated image. Captions are post-production overlays.

## Lens Guide

| Lens equivalent | Use | Visual feel |
|---|---|---|
| 24mm | large room, distant interview, architecture, strong negative space | expansive, observational, real estate-like if overused |
| 28mm | iPhone default documentary, table/workspace/lifestyle | candid, close to how phones see scenes |
| 35mm | premium founder conversation, medium-wide portrait, interview | natural, balanced, safest default |
| 50mm | side profile, listening, podium/podcast, emotional compression | intimate, compressed background |
| 77mm | close profile, stage/podcast, bokeh-heavy lifestyle | polished, selective, less iPhone-default |

## Archetypes

### distant_interview_room

Use for: the "someone is interviewing the subject" signal, high-trust founder coaching, selling/positioning lessons.

Camera recipe:

- Lens: 24mm or 28mm equivalent.
- Camera height: seated eye level or slightly high, as if held by a person standing/sitting across the room.
- Angle: wide room composition, the subject small-to-medium in frame, listener visible in foreground or opposite chair.
- Subject placement: the subject on lower-left or lower-right third, with tall wall/window negative space above.
- Blocking: include listener from behind, office chair silhouette, crossed leg, shoulder, or back of head on the opposite side.
- Light: tall-window daylight, long rectangular shadows, soft haze through glass, white/concrete room.
- Prompt keywords: `wide observational interview frame`, `another person seated across from the subject`, `large clean architectural negative space`, `documentary behind-the-scenes`.

Failure modes:

- The subject becomes too tiny or unrecognizable.
- Image becomes an empty architecture shot.
- Listener becomes too dominant.

### over_shoulder_founder_table

Use for: founder advice, consulting, strategy, product/workflow walkthroughs.

Camera recipe:

- Lens: 28mm or 35mm equivalent.
- Camera height: seated eye level, slightly above table.
- Angle: over-the-shoulder from the other person's side.
- Subject placement: the subject across the table, face visible, laptop/phone/notebook in the lower frame.
- Blocking: soft foreground shoulder, hand, laptop corner, or notebook edge proving the viewer is seated in the conversation.
- Light: office/coworking daylight, glass wall, warm-neutral indoor practicals.
- Prompt keywords: `camera positioned beside the listener`, `foreground listener shoulder softly blurred`, `the subject explaining across a small table`.

Failure modes:

- It turns into a corporate stock meeting.
- Foreground blocks the subject's face.
- Too many readable UI screens or logos appear.

### workspace_turnback

Use for: students, knowledge, building, coding, creator operations, "caught in the middle of work".

Camera recipe:

- Lens: 28mm or 35mm equivalent.
- Camera height: seated or standing chest height behind/side of the subject.
- Angle: three-quarter rear or side-rear, the subject turns back toward someone speaking.
- Subject placement: the subject foreground-middle, work desk and monitors behind or beside them.
- Blocking: desk, monitor glow, mouse, keyboard, laptop, blurred code-like panels with no readable text.
- Light: mixed office light, muted warm/cool balance, slight grain.
- Prompt keywords: `caught mid-conversation while working`, `turning back from desk`, `documentary office still`.

Failure modes:

- Readable code/text appears.
- Monitor becomes the subject instead of the person.
- Outfit drifts into hoodie unless requested.

### side_profile_listening

Use for: reflective ideas, premium audience, time, confidence, masculinity/identity, quiet persuasion.

Camera recipe:

- Lens: 50mm or 77mm equivalent.
- Camera height: eye level.
- Angle: close side profile or three-quarter profile.
- Subject placement: profile on one third with background bokeh or dark negative space.
- Blocking: blurred foreground plant, glass reflection, palm lights, table edge, or another person's shoulder.
- Light: warm sunset, window side light, practical lamps, deep shadows.
- Prompt keywords: `close side-profile listening shot`, `shallow depth of field`, `warm practical bokeh`, `quiet conversation off-camera`.

Failure modes:

- Becomes a posed glamour portrait.
- Background becomes too decorative or fantasy-like.
- Face identity drifts due to profile angle.

### rear_silhouette_window

Use for: freedom, leverage, time, founder loneliness, high-rise reflection, future-facing strategy.

Camera recipe:

- Lens: 35mm or 50mm equivalent.
- Camera height: standing eye level.
- Angle: rear silhouette or rear three-quarter at a window.
- Subject placement: the subject centered or on one third, city skyline blurred beyond glass.
- Blocking: window frame, reflections, desk edge, soft city bokeh.
- Light: night city practicals, subject mostly dark, readable body outline.
- Prompt keywords: `rear silhouette at high-rise window`, `city lights`, `quiet reflective founder moment`.

Failure modes:

- Identity is not visible enough if no face angle is included.
- Scene becomes luxury real estate advertising.
- Cyberpunk color overpowers realism.

### sunlit_chair_direct

Use for: "rich people", clear positioning hooks, premium interview first frame.

Camera recipe:

- Lens: 35mm or 50mm equivalent.
- Camera height: seated eye level or slightly low.
- Angle: frontal or slight three-quarter, medium-wide.
- Subject placement: the subject on right third or centered-right; large blank wall/floor area on left for overlay copy.
- Blocking: simple chair, floor shadows, white wall, concrete floor.
- Light: hard window sun with geometric shadows, soft fill, quiet minimal room.
- Prompt keywords: `minimal studio chair interview`, `large clean negative space`, `hard rectangular window shadows`.

Failure modes:

- Too staged and emotionless.
- Body proportions become overly muscular.
- Room becomes sterile stock-photo set.

### lifestyle_two_shot

Use for: lifestyle, social proof, offline relationships, product/service outcomes.

Camera recipe:

- Lens: 28mm or 35mm equivalent.
- Camera height: chest or eye level.
- Angle: candid two-shot beside an object such as car, cafe table, balcony, event hallway, or studio doorway.
- Subject placement: the subject interacting with another person; both are partially casual, not posed.
- Blocking: one person partly cropped, car/door/table edge creates foreground depth.
- Light: late afternoon sun or soft outdoor shade, warm natural highlights.
- Prompt keywords: `candid two-person lifestyle conversation`, `shot by a friend standing nearby`, `not posed, mid-laugh or mid-explanation`.

Failure modes:

- Becomes influencer car flex.
- Extra person competes with the subject's identity.
- Logos and readable clothing text appear.

## Camera Quality Defaults

Use one of these quality profiles:

### iphone_video_still

```text
Shot by another person on an iPhone 15 Pro / iPhone 16 Pro as a documentary video still, natural handheld framing, slight motion softness, realistic sensor noise, subtle HDR, not overly sharp, not studio-polished.
```

### premium_documentary

```text
Premium founder documentary look, natural available light, soft contrast, muted warm-neutral grade, real skin texture, restrained shallow depth of field, believable shadows, no stock-photo posing.
```

### social_screenshot_frame

```text
Looks like a frame pulled from a high-quality Instagram Reel or founder mini-documentary, with clean composition for overlay text, no baked-in captions, and realistic phone-camera compression.
```

## Prompt Snippets

### Conversation Proof

```text
Make it obvious another person is present: include a soft out-of-focus listener shoulder, back of head, chair, hand, or laptop edge in the foreground. The subject looks toward that person, not into camera.
```

### Overlay-Safe Space

```text
Leave clean negative space across the upper middle or left side for future text overlay, but do not generate any text now.
```

### Realism Lock

```text
This should feel like a real behind-the-scenes photo taken during a founder conversation, with slight handheld imperfection, natural light, realistic skin texture, and no glossy advertisement styling.
```

## Example Prompt: Distant Interview Room

```text
Create a realistic candid iPhone documentary photo still using the attached subject face references as the identity lock.

Native 16:9 composition for a social video frame. No text, no captions, no logo, no UI overlay, no watermark. Leave clean negative space across the tall glass wall for future overlay copy.

Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt) — and preserve facial proportions and hairline across angles.

Scene: the subject sits on a simple warm brown fabric chair in a bright minimal studio with tall glass windows, white architectural columns, concrete floor, and long rectangular sunlight shadows. They are mid-conversation, leaning forward slightly, one hand gesturing calmly. A second person is visible from behind on the opposite side of the room, seated in a dark office chair, softly out of focus.

Camera: shot by another person on an iPhone 15 Pro as a documentary video still. Lens 24mm equivalent, wide observational interview frame, camera at seated eye level from across the room, the subject placed on the lower-left third, listener silhouette on the right foreground, large clean architectural negative space above and between them.

Light and quality: natural window daylight, soft haze through glass, muted warm-neutral color grade, soft contrast, realistic shadows, slight sensor noise, subtle handheld imperfection, premium founder documentary feel.

Negative: no readable text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not change identity, do not add facial hair, glasses, hats, suit styling, exaggerated jawline, plastic skin, distorted eyes, cropped head, extra fingers, warped hands, inconsistent hairline, or duplicate the subject.
```

### monochrome_work_desk

Use for: Deep work, focus, process, late-night grinding.

Camera recipe:

- Lens: 28mm or 35mm equivalent.
- Camera height: Seated chest height.
- Angle: Frontal or slight 3/4.
- Subject placement: Centered or slightly off-center.
- Blocking: Laptop on desk, dark background, possible blurred foreground object.
- Light: Low-key, monochrome, soft overhead/falloff light, visible grain.
- Prompt keywords: `monochrome documentary work still`, `black and white`, `hunched over laptop`, `deep shadows`, `focused work tunnel`.

Failure modes:

- Image becomes artificially crushed instead of filmic.
- Subject looks posed rather than actively working.

### architectural_corridor_walk

Use for: Premium movement, authority, institutional scale.

Camera recipe:

- Lens: 24mm or 35mm equivalent.
- Camera height: Standing chest or eye level.
- Angle: Frontal or slight 3/4.
- Subject placement: Centered or lower-middle, small in frame.
- Blocking: Walking candidly, hands in pockets or holding simple object.
- Light: Soft daylight, pale neutral concrete, bright window side, strong diagonal shadows.
- Prompt keywords: `full-body walk`, `bright concrete corridor`, `architectural daylight`, `editorial cleanliness`.

Failure modes:

- Subject becomes too tiny or unrecognizable.
- Scene becomes luxury real estate advertising.

### tiny_chair_blank_wall

Use for: Text-overlay-first frames, extreme minimalism.

Camera recipe:

- Lens: 24mm or 35mm equivalent.
- Camera height: Seated eye level.
- Angle: Frontal.
- Subject placement: Lower-middle, small in frame.
- Blocking: Single low chair, huge white wall above.
- Light: Soft natural daylight, high-key minimalism.
- Prompt keywords: `tiny subject in low chair`, `huge blank white wall`, `extreme negative space`, `minimalist editorial`.

Failure modes:

- Wall texture looks fake or AI-generated.
- Subject posture looks awkward or uncomfortable.

### side_writing_table

Use for: Thinking, planning, reflection, intimate documentary feel.

Camera recipe:

- Lens: 35mm or 50mm equivalent.
- Camera height: Seated eye level.
- Angle: Side profile or 3/4 profile.
- Subject placement: Off-center, leading lines from table.
- Blocking: Writing by hand, books/notebook in foreground.
- Light: Warm side daylight, domestic/studio calm, shallow depth.
- Prompt keywords: `side-writing table`, `writing by hand`, `warm window light`, `books and notebook`, `shallow depth of field`.

Failure modes:

- Table becomes cluttered with random AI objects.
- Subject looks posed instead of actively writing.

### team_workshop_discussion

Use for: Social proof, collaboration, creative workshop realism.

Camera recipe:

- Lens: 28mm or 35mm equivalent.
- Camera height: Standing or seated eye level.
- Angle: 3/4 or side angle.
- Subject placement: Off-center, interacting with others.
- Blocking: Standing speaker, others blurred in background or foreground.
- Light: Documentary monochrome, indoor available light.
- Prompt keywords: `team workshop discussion`, `monochrome documentary`, `standing speaker`, `others blurred in background`, `casual collaboration`.

Failure modes:

- Other people look like duplicates of the subject.
- Scene looks like a posed corporate stock photo.

### audience_view_keynote

Use for: Teaching, authority, scale, event documentation.

Camera recipe:

- Lens: 50mm or 77mm equivalent.
- Camera height: Audience seated eye level.
- Angle: From audience perspective.
- Subject placement: Distant, on stage or podium.
- Blocking: Crowd heads in foreground, speaker distant.
- Light: Monochrome event documentation, high-ceiling room.
- Prompt keywords: `audience-view keynote`, `speaker distant`, `crowd heads foreground`, `monochrome event documentation`.

Failure modes:

- Foreground heads block the speaker completely.
- Speaker becomes unrecognizable.

### stage_spotlight_speaker

Use for: Premium authority, dramatic stage presence.

Camera recipe:

- Lens: 50mm or 77mm equivalent.
- Camera height: Stage level or slightly below.
- Angle: Frontal or slight 3/4.
- Subject placement: Centered or slightly off-center.
- Blocking: Hands gesturing, earpiece or lavalier mic.
- Light: Monochrome stage spot, bokeh stage lights behind, dramatic contrast.
- Prompt keywords: `stage spotlight speaker`, `monochrome stage spot`, `bokeh stage lights`, `dramatic contrast`, `earpiece mic`.

Failure modes:

- Contrast is too harsh, losing facial details.
- Gesture looks unnatural or AI-warped.

### doorframe_event_speaker

Use for: Candid event documentation, "shot by observer" realism.

Camera recipe:

- Lens: 35mm or 50mm equivalent.
- Camera height: Standing eye level.
- Angle: Shot from side of room through doorframe/gap.
- Subject placement: Off-center, framed by architecture.
- Blocking: Handheld mic, audience visible in background.
- Light: Warm indoor event track lights, film-grain feel.
- Prompt keywords: `shot through doorframe`, `warm event track lights`, `handheld mic`, `audience depth`, `film-grain feel`.

Failure modes:

- Doorframe blocks too much of the scene.
- Lighting looks like a generic studio rather than an event.

### panel_lounge_speaker

Use for: Thought leadership, panel discussion, event atmosphere.

Camera recipe:

- Lens: 35mm or 50mm equivalent.
- Camera height: Seated eye level.
- Angle: Frontal or slight 3/4.
- Subject placement: Seated in lounge chair.
- Blocking: Handheld mic, coffee cup/water in foreground, large screen behind.
- Light: Warm stage event light.
- Prompt keywords: `panel lounge speaker`, `seated with handheld mic`, `warm stage event light`, `coffee cup foreground`, `large screen behind`.

Failure modes:

- Screen behind contains readable (but nonsensical) text.
- Foreground objects look like AI artifacts.
