# Detailed Prompt Recipes

Use these recipes when the user wants reference-image / image-to-image prompts that match high-quality founder-video stills: premium composition, strong camera blocking, natural but intentional lighting, realistic video-frame texture, and clear evidence that another person is filming or participating.

## Reference Style Study

The examples share these traits:

- Quality: high-end social video stills, not phone snapshots in the casual low-quality sense. They look like iPhone/compact cinema footage graded for Instagram.
- Camera: mostly 24-50mm equivalent. Wide frames use 24/28mm; table and workspace frames use 28/35mm; profile and lifestyle mood frames use 50/77mm.
- Angle: camera is rarely neutral straight-on. It is across the room, over a listener's shoulder, side-profile, rear silhouette, or handheld beside another person.
- Blocking: another person is often implied through foreground shoulder/head/hand, an opposite chair, a table edge, a car, or an off-camera eyeline.
- Subject behavior: the main character is speaking, listening, thinking, looking toward someone, or caught mid-work. They are not posing for a headshot.
- Light: available light that still feels controlled: window daylight, hard rectangular sun, warm practicals, night skyline bokeh, stage/podcast light, outdoor golden hour.
- Grade: warm-neutral, muted, slightly underexposed, soft contrast, realistic shadow detail, moderate grain/noise, no over-sharp AI skin.
- Copy space: most frames have clean negative space or dark mid-frame areas where text can be overlaid later.

## Validated Defaults

Use these defaults when generating a first review batch:

- Aspect: native `16:9`.
- Review output: `1920x1080`.
- Provider resolution: `2K`.
- Reference images: 4 subject face references, preferably front neutral, three-quarter, side angle, and thinking.
- First three archetypes: `distant_interview_room`, `over_shoulder_founder_table`, `side_profile_listening`.

Example batch output folder:

```text
assets/generated-social/cinematic-video-stills-YYYY-MM-DD/
```

What worked:

- 16:9 produced stronger video-frame realism than 4:5.
- Explicit foreground listener language worked: the generated images included an opposite chair, over-shoulder listener, or foreground hand.
- A single consistent wardrobe identity lock was followed across all three.
- No baked-in text appeared when the prompt repeatedly said raw photo/video-frame reference only.

What to keep tightening:

- Say `do not let the foreground object cover the subject's face` in every conversation prompt.
- Use `not glossy stock photo, not studio headshot, not AI portrait` in every quality block.
- Keep table screens and monitors abstract; do not ask for readable dashboards or code.

## Universal Quality Lock

Add this to every prompt unless it conflicts with the scene:

```text
High-quality social video still, shot by another person on iPhone 15 Pro / iPhone 16 Pro ProRes or a compact mirrorless documentary camera, natural handheld framing, realistic optical depth, subtle lens softness, real skin texture, gentle sensor noise, muted warm-neutral color grade, soft contrast, controlled highlights, believable shadows. Premium founder/operator documentary feel, not a glossy stock photo, not a studio headshot, not an AI portrait.
```

## Universal Negative Lock

```text
No text, no generated captions, no fake glyphs, no UI words, no logos, no watermarks, no poster typography, no QR code, no product ad layout, no over-sharpened HDR, no plastic skin, no waxy face, no celebrity glamour, no fashion editorial pose. Do not add facial hair, glasses, hats, earrings, heavy makeup, tattoos, suit styling, exaggerated jawline, distorted eyes, cropped head, extra fingers, warped hands, inconsistent hairline, duplicate the subject, or a second lookalike.
```

## Prompt Recipe 1: Distant Interview Room

Use when the shot must clearly feel like another person is interviewing the subject.

Camera recipe:

- Aspect: 16:9 first. Can crop to 4:5 later if needed.
- Lens: 24mm equivalent for tall room geometry; 28mm if the subject must be more readable.
- Camera height: seated eye level or slightly above seated eye level.
- Distance: 4-7 meters away from the subject.
- Angle: wide observational frame across the room.
- Main character angle: the subject 3/4 front, looking toward the listener, not into camera.
- Other person: visible from behind on the opposite side, dark chair silhouette or shoulder/head.
- Focus: the subject reasonably sharp, listener softer, architecture readable.
- Light: tall-window daylight, hard sun rectangles, soft haze, pale concrete/white walls.

Prompt:

```text
Create a high-quality realistic documentary video still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame, no text, no captions, no logo, no UI overlay, no watermark. Leave large clean negative space across the tall window/wall area for later overlay copy.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt). Preserve facial proportions and hairline across angles.

SCENE:
The subject sits on a simple warm brown fabric chair inside a bright minimal studio or founder interview space with tall glass windows, white architectural columns, polished concrete floor, and long rectangular sunlight shadows. They are mid-conversation, leaning forward slightly, one hand gesturing calmly as if answering a thoughtful question.

CAMERA:
Shot by another person from across the room, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 24mm equivalent, wide observational interview frame, camera at seated eye level about 5 meters away. The subject is placed on the lower-left third, small-to-medium in frame. A second person is visible from behind on the right foreground in a dark office chair, softly out of focus, proving this is a real conversation. Do not let the foreground listener block the subject's face.

LIGHT / QUALITY:
High-quality social video still, natural tall-window daylight, soft haze through glass, controlled highlights, realistic concrete-floor shadows, muted warm-neutral grade, soft contrast, subtle lens softness, gentle sensor noise, real skin texture, premium founder/operator documentary feel.

NEGATIVE:
No text, no generated captions, no fake glyphs, no UI words, no logos, no watermarks, no poster typography, no QR code, no product ad layout. Do not change identity, do not add facial hair, glasses, hats, suit styling, exaggerated jawline, plastic skin, distorted eyes, cropped head, extra fingers, warped hands, inconsistent hairline, duplicate the subject, or another lookalike.
```

## Prompt Recipe 2: Over-Shoulder Founder Table

Use for founders, strategy, advisory, product walkthroughs, and sales/consulting positioning.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 28mm or 35mm equivalent.
- Camera height: seated eye level, just above table height.
- Distance: 1-2 meters.
- Angle: from beside/behind the listener, over the shoulder.
- Main character angle: the subject across the table, 3/4 front, eyes looking toward listener or laptop.
- Other person: foreground shoulder, hand, laptop edge, notebook, or blurred head.
- Focus: the subject's face sharp, foreground listener soft, table props readable as objects but not text.
- Light: glass-wall office daylight or warm small meeting room practicals.

Prompt:

```text
Create a high-quality realistic candid founder conversation still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame, raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Keep clean negative space in the upper wall/window area for later text overlay.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject is seated across a compact cafe/coworking meeting table with a laptop, phone, notebook, and coffee cup. They are explaining a practical founder strategy, leaning forward slightly with one small hand gesture. The setting feels like a real advisory conversation, not a corporate stock meeting.

CAMERA:
Shot by or beside the other person in the conversation, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 35mm equivalent, seated eye-level over-the-shoulder angle from the listener's side. Include a soft out-of-focus foreground listener shoulder, hand, or laptop edge in the lower/right frame. The subject is across the table on the opposite third, face sharp, looking toward the listener rather than directly into camera.

LIGHT / QUALITY:
High-end social video still, natural office window light with warm indoor practical fill, realistic optical depth, soft contrast, muted warm-neutral color grade, controlled highlights on glass and table, real skin texture, slight handheld imperfection and gentle sensor noise.

NEGATIVE:
No readable screen text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code, no product ad layout. Do not let the foreground object cover the subject's face. Avoid corporate boardroom stock-photo posing, extra fingers, warped hands, identity drift, facial hair, glasses, suit styling, plastic skin, or duplicate the subject.
```

## Prompt Recipe 3: Workspace Turnback

Use for students, knowledge, coding, building, and "caught mid-work" scenes.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 28mm/35mm equivalent.
- Camera height: chest height or seated shoulder height.
- Distance: 1-1.5 meters.
- Angle: rear-side angle; the subject turns back from the desk toward someone.
- Main character angle: side-rear 3/4; face visible in profile/three-quarter.
- Blocking: monitors, desk, blurred code-like light patterns with no readable text.
- Focus: face and shoulder sharp, desk slightly soft.
- Light: office practicals, monitor glow, warm/cool mixed light.

Prompt:

```text
Create a high-quality realistic documentary workspace still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt) unless another outfit is explicitly requested.

SCENE:
The subject is at a real founder/operator desk with laptop, monitor, keyboard, mouse, notebook, water bottle, and scattered work objects. They have just turned back from the desk toward someone speaking off-camera, as if explaining a technical workflow or answering a student question. The monitor may show abstract code-like blocks or dashboard shapes, but no readable text.

CAMERA:
Shot by another person standing slightly behind and beside the subject, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 28mm or 35mm equivalent, chest-height camera, close medium-wide rear-side angle. The subject's shoulder and side profile dominate the foreground, face visible in three-quarter turn, eyes looking toward the off-camera listener. Desk and monitors create depth behind them.

LIGHT / QUALITY:
High-quality social video still, mixed practical office light and soft monitor glow, muted warm/cool balance, realistic shadows under desk, subtle grain, natural lens softness, real skin texture, not overly sharp, premium behind-the-scenes founder/operator mood.

NEGATIVE:
No readable code, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no UI words, no QR code. Do not turn this into a staged tech stock photo. Avoid hoodie drift unless requested, facial hair, glasses, distorted hands, cropped head, plastic skin, inconsistent hairline, or duplicate the subject.
```

## Prompt Recipe 4: Side-Profile Listening

Use for time, confidence, premium audience, quiet persuasion, and emotional/interior moments.

Camera recipe:

- Aspect: 16:9 preferred.
- Lens: 50mm or 77mm equivalent.
- Camera height: eye level.
- Distance: 0.8-1.5 meters.
- Angle: side profile or close 3/4 profile.
- Main character angle: listening, not speaking loudly; eyes toward someone off-frame.
- Blocking: blurred foreground plant, glass edge, table, microphone, or another person's hand.
- Focus: face/eye sharp, background bokeh strong.
- Light: warm practicals, side window light, sunset, or low-key interior.

Prompt:

```text
Create a high-quality realistic close side-profile documentary still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame. Raw video-frame reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave clean dark or softly blurred space near the center/lower third for future overlay copy.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject is seated in a quiet premium indoor or outdoor evening setting, listening to someone just off-camera. They are calm, thoughtful, and practical, with a small relaxed hand position near the table or chin. Background lights are warm and softly blurred, suggesting a real conversation after a founder meeting.

CAMERA:
Shot by another person nearby, compact mirrorless documentary camera or iPhone 16 Pro telephoto video still. Lens 50mm or 77mm equivalent, eye-level close side-profile angle, shallow depth of field. The subject's face is on the left or right third, profile sharp, eyes looking toward the off-camera speaker. Include a soft foreground edge such as a glass reflection, plant, table edge, or blurred listener hand to create depth.

LIGHT / QUALITY:
High-end social video still, warm practical bokeh, low-key side light, realistic skin texture, controlled highlights, soft shadow falloff, muted warm grade, subtle grain, natural lens softness, premium documentary mood without fashion-ad posing.

NEGATIVE:
No text, no captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not glamorize into a celebrity portrait. Avoid over-sculpted jaw, facial hair, glasses, hats, plastic skin, distorted eyes, cropped head, warped hands, inconsistent hairline, duplicate the subject, or fantasy background.
```

## Prompt Recipe 5: Rear Silhouette Window

Use for freedom, time, leverage, founder reflection, and high-rise city metaphors.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 35mm or 50mm equivalent.
- Camera height: standing eye level.
- Distance: 2-4 meters.
- Angle: rear silhouette or rear 3/4 at window.
- Main character angle: back to camera, slight head turn optional for identity hint.
- Blocking: window frame, skyline bokeh, glass reflection.
- Focus: body outline sharp, skyline soft.
- Light: night city bokeh, dark subject silhouette, gentle rim light.

Prompt:

```text
Create a high-quality realistic night window documentary still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave clean dark negative space over the subject's back or window area for future text overlay.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, and a consistent wardrobe item (for example a plain solid-color T-shirt), visible in slight profile if the face turns.

SCENE:
The subject stands near a large high-rise window at night, looking out at a blurred city skyline and harbour lights. They are quiet and reflective, holding a phone loosely or resting one hand near the window ledge. The moment feels like a founder thinking about freedom, leverage, and time after work.

CAMERA:
Shot by another person standing a few meters behind them, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 35mm or 50mm equivalent, standing eye-level rear silhouette or rear three-quarter angle. The subject is centered or on one third, body outline readable, city lights soft beyond glass, optional slight head turn showing a hint of profile without making them pose.

LIGHT / QUALITY:
High-quality social video still, natural night city bokeh, low-key exposure, subtle rim light from window/city, controlled highlights, deep navy shadows, realistic glass reflections, muted cinematic grade, gentle sensor noise, no cyberpunk exaggeration.

NEGATIVE:
No readable text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not turn it into a luxury real estate ad or cyberpunk scene. Avoid identity drift, duplicate the subject, facial hair, glasses, hats, suit styling, plastic skin, distorted body, or unreadable muddy silhouette.
```

## Prompt Recipe 6: Sunlit Chair Direct

Use for a direct hook frame with premium positioning and clean overlay space.

Camera recipe:

- Aspect: 16:9 first; 4:5 works for feed.
- Lens: 35mm or 50mm equivalent.
- Camera height: seated eye level or slightly low.
- Distance: 2-4 meters.
- Angle: frontal or slight 3/4.
- Main character angle: the subject faces interviewer, not necessarily camera; hands relaxed or clasped.
- Blocking: simple chair, clean wall/floor, geometric shadows.
- Focus: whole seated body sharp enough.
- Light: hard daylight through window, large shadow shapes, soft fill.

Prompt:

```text
Create a high-quality realistic founder interview still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave a large clean blank wall or floor area on the left/center for future overlay copy.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject sits alone on a simple warm brown chair in a minimal white/concrete studio with tall window light and long rectangular shadows. They are in a serious but calm founder interview moment, leaning forward slightly with hands relaxed or lightly clasped, looking toward an interviewer just off-camera.

CAMERA:
Shot by another person on iPhone 15 Pro / iPhone 16 Pro ProRes or compact mirrorless documentary camera. Lens 35mm or 50mm equivalent, medium-wide seated interview frame, camera at seated eye level or slightly low, the subject placed on the right third or centered-right. The composition uses clean negative space and architectural shadows, not decorative props.

LIGHT / QUALITY:
High-end social video still, hard window sunlight with geometric wall/floor shadows, soft ambient fill, realistic skin texture, controlled highlight rolloff, muted warm-neutral grade, soft contrast, gentle grain, premium founder documentary feel.

NEGATIVE:
No text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not make the subject too muscular, older, celebrity-like, emotionless, or corporate. Avoid plastic skin, distorted hands, cropped head, extra fingers, inconsistent hairline, suit styling, or duplicate the subject.
```

## Prompt Recipe 7: Lifestyle Two-Shot

Use for lifestyle, trust, offline relationships, "selling lifestyle", and social proof scenes.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 28mm/35mm equivalent.
- Camera height: chest height or eye level.
- Distance: 1-3 meters.
- Angle: handheld nearby friend angle, slightly imperfect.
- Main character angle: the subject interacting with another person, not performing to camera.
- Blocking: car/table/doorway/person partly cropped.
- Focus: the subject and second person both acceptable; background gently soft.
- Light: golden hour/outdoor shade/warm daylight.

Prompt:

```text
Create a high-quality realistic candid lifestyle conversation still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt) unless another simple casual outfit is requested.

SCENE:
The subject is outdoors or in a semi-outdoor lifestyle setting, casually speaking with one other person beside a car, cafe table, balcony, studio doorway, or event hallway. The moment is mid-conversation, relaxed and natural, not a posed influencer photo. One person may be partly cropped to make the camera feel handheld and close to the scene.

CAMERA:
Shot by a nearby friend or team member on iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 28mm or 35mm equivalent, chest-height handheld angle, slight natural tilt or imperfect framing, the subject on one third interacting with the other person. Use foreground depth from a car door, table edge, doorway, or partially cropped shoulder. Keep the subject's face readable and identity consistent.

LIGHT / QUALITY:
High-quality social video still, late afternoon sun or soft outdoor shade, warm natural highlights, realistic skin texture, muted warm grade, soft contrast, slight handheld motion softness, gentle sensor noise, premium but real lifestyle documentary feel.

NEGATIVE:
No readable clothing logos, no generated captions, no fake glyphs, no watermarks, no poster typography, no QR code. Do not turn it into a car-flex influencer ad. Avoid extra people crowding the scene, identity drift, duplicate the subject, facial hair, glasses, suit styling, plastic skin, distorted hands, or cropped face.
```

## Batch Construction

For a first review batch, choose three distinct visual jobs:

1. `distant_interview_room` for the strongest conversation/interviewer signal.
2. `over_shoulder_founder_table` for consulting/founder strategy.
3. `side_profile_listening` or `rear_silhouette_window` for emotional premium mood.

Only continue to lifestyle/workspace variants after reviewing identity, realism, and camera quality from the first batch.

## QA Rubric For Generated Batches

Accept when:

- The output reads as a frame shot by another person during a real conversation.
- The subject's hair, face shape, wardrobe, and calm operator expression are broadly consistent.
- The image has premium social-video quality: controlled light, realistic skin, soft contrast, and subtle grain.
- The composition has usable copy space for later overlays.
- No generated text, logos, QR codes, readable UI, or fake glyphs are present.

Revise when:

- The photo becomes a posed headshot or corporate stock meeting.
- The other person blocks the subject's face or competes as the main subject.
- The subject looks older, muscular, celebrity-like, or over-glamourized.
- The output has plastic skin, warped hands, inconsistent hairline, or multiple lookalike people.

## Prompt Recipe 8: Monochrome Work Desk

Use for deep work, focus, process, and late-night grinding.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 28mm or 35mm equivalent.
- Camera height: Seated chest height.
- Distance: 1-2 meters.
- Angle: Frontal or slight 3/4.
- Main character angle: Hunched over laptop, focused.
- Blocking: Laptop on desk, dark background, possible blurred foreground object.
- Focus: Subject sharp, background dark/soft.
- Light: Low-key, monochrome, soft overhead/falloff light, visible grain.

Prompt:

```text
Create a high-quality realistic monochrome documentary work still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave dark negative space in the background for future overlay copy.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject is seated at a desk, hunched over a laptop, deep in focused work. The setting is minimal, with a dark background. A blurred foreground object, like a cup or notebook, adds depth. The mood is intense, process-oriented, and candid.

CAMERA:
Shot by another person nearby, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 28mm or 35mm equivalent, seated chest-height angle. The subject is centered or slightly off-center, face illuminated by the laptop screen or soft overhead light.

LIGHT / QUALITY:
High-quality social video still, black and white documentary style, low-key lighting, soft overhead or screen falloff light, visible film grain, deep shadows, controlled highlights, premium operator documentary feel.

NEGATIVE:
No readable text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not make the image look artificially crushed. Avoid identity drift, duplicate the subject, facial hair, glasses, hats, suit styling, plastic skin, or distorted hands.
```

## Prompt Recipe 9: Architectural Corridor Walk

Use for premium movement, authority, and institutional scale.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 24mm or 35mm equivalent.
- Camera height: Standing chest or eye level.
- Distance: 3-5 meters.
- Angle: Frontal or slight 3/4.
- Main character angle: Walking candidly, not looking at camera.
- Blocking: Hands in pockets or holding simple object, bright corridor.
- Focus: Subject sharp, corridor leading lines clear.
- Light: Soft daylight, pale neutral concrete, bright window side, strong diagonal shadows.

Prompt:

```text
Create a high-quality realistic architectural documentary still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave clean negative space on the walls or floor for future text overlay.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject is walking candidly through a bright, clean, minimalist architectural corridor. They have their hands in their pockets or are holding a simple object like a phone or notebook. They are not looking at the camera, conveying a sense of premium movement and authority.

CAMERA:
Shot by another person from a distance, iPhone 15 Pro / iPhone 16 Pro ProRes documentary video still. Lens 24mm or 35mm equivalent, standing chest or eye-level angle. The subject is centered or lower-middle, small in the frame, emphasizing the scale of the environment.

LIGHT / QUALITY:
High-quality social video still, soft daylight, pale neutral concrete, bright window side, strong diagonal architectural shadows, low-saturation editorial cleanliness, realistic skin texture, muted warm-neutral grade.

NEGATIVE:
No readable text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not turn the scene into a luxury real estate ad. Avoid identity drift, duplicate the subject, facial hair, glasses, hats, suit styling, plastic skin, or distorted body proportions.
```

## Prompt Recipe 10: Stage Spotlight Speaker

Use for premium authority, dramatic stage presence, and event documentation.

Camera recipe:

- Aspect: 16:9 or 4:5.
- Lens: 50mm or 77mm equivalent.
- Camera height: Stage level or slightly below.
- Distance: 2-4 meters.
- Angle: Frontal or slight 3/4.
- Main character angle: Speaking, gesturing with hands.
- Blocking: Earpiece or lavalier mic, dark stage background.
- Focus: Subject sharp, background bokeh.
- Light: Monochrome stage spot, bokeh stage lights behind, dramatic contrast.

Prompt:

```text
Create a high-quality realistic monochrome stage documentary still using the attached subject face references as the identity lock.

FORMAT:
Native 16:9 cinematic social video frame or 4:5 Instagram feed frame. Raw photo/video reference only. No text, no captions, no logos, no UI overlay, no watermark. Leave dark negative space around the subject for future overlay copy.

IDENTITY:
Keep the same subject identity from the provided face references. Describe your subject's fixed traits here — approximate age range, hair, face shape, skin tone, default expression, and a consistent wardrobe item (for example a plain solid-color T-shirt).

SCENE:
The subject is speaking on a dark stage, conveying premium authority. They are gesturing naturally with their hands and wearing a subtle earpiece or lavalier mic. The background is dark, with soft bokeh from distant stage lights.

CAMERA:
Shot by an event photographer, compact mirrorless documentary camera. Lens 50mm or 77mm equivalent, stage level or slightly below angle. The subject is centered or slightly off-center, framed to capture the gesture and expression.

LIGHT / QUALITY:
High-quality event documentary still, black and white, dramatic stage spotlight, bokeh stage lights in the background, strong cinematic contrast, visible film grain, controlled highlights, realistic skin texture.

NEGATIVE:
No readable text, no generated captions, no fake glyphs, no logos, no watermarks, no poster typography, no QR code. Do not make the contrast so harsh that facial details are lost. Avoid unnatural or AI-warped hand gestures, identity drift, duplicate the subject, facial hair, glasses, hats, suit styling, or plastic skin.
```
