# Art Direction Matrix

Use this when designing or prompting visual comps. Choose deliberately; do not combine everything.

## Design Dials

Set each dial from 1 to 10:

- Visual ambition: 1-3 restrained utility, 4-6 commercial clarity, 7-8 premium creative, 9-10 experimental. For product UI, reduce to 4-7 unless the surface is a showcase or onboarding moment.
- Information density: 1-3 luxury/editorial, 4-6 normal SaaS or marketing, 7-8 dashboards and operational tools, 9-10 command-center views. Keep product UI density high enough for repeated work; keep brand pages sparse enough for persuasion.
- Image reliance: 1-3 app utility and text-led interfaces, 4-6 product screenshots or diagrams, 7-8 marketing/editorial media, 9-10 portfolio/ecommerce where the image is the product.
- Motion level: 1-3 static trust and fast product use, 4-6 microinteraction and state feedback, 7-8 scroll narrative, 9-10 advanced canvas/WebGL/GSAP work. For product UI, motion must explain state or reduce perceived latency.
- Conversion discipline: 1-3 exploratory/editorial, 4-6 brand site, 7-8 landing page, 9-10 paid acquisition or checkout. Higher values require fewer competing CTAs and clearer proof.
- Implementation clarity: 1-3 concept art, 4-6 buildable with interpretation, 7-8 implementation-ready spec, 9-10 directly shippable code guidance. Keep at 8+ unless the user explicitly asks for pure exploration.
- Brand fidelity: 1-3 loose inspiration, 4-6 recognizable but flexible, 7-8 on-brand, 9-10 strict adherence to the brand's tone, language, color logic, and text-branding rules.

## Register Defaults

Use the register to bias the dials before choosing visual patterns.

- `brand`: marketing, landing, creator, campaign, portfolio, product-story, and editorial pages. Defaults: ambition 7, density 4, image reliance 7, motion 5, conversion 7, implementation clarity 8, brand fidelity 8.
- `product`: dashboards, tools, admin panels, settings, forms, onboarding, data views, and workflow surfaces. Defaults: ambition 5, density 7, image reliance 3, motion 3, conversion 5, implementation clarity 9, brand fidelity 7.
- If the page blends both, let the first viewport follow `brand` and the working interface sections follow `product`.

When reducing scope, cut decorative motion, material complexity, or experimental layout before cutting accessibility, responsive behavior, state coverage, or copy clarity.

## Review Mode Shortcuts

- `shape`: lock register, dials, thesis, route/section map, component jobs, and acceptance criteria.
- `critique`: score hierarchy, clarity, brand fit, UX friction, accessibility, and generic-AI tells.
- `polish`: improve spacing rhythm, typography, color balance, component consistency, and final responsive fit.
- `harden`: cover loading, empty, error, disabled, focus, long text, i18n, reduced motion, and performance.
- `typeset`: inspect font choice, scale contrast, line length, multilingual/CJK readability, button wrapping, and label hierarchy.
- `layout`: inspect grid logic, scan order, image framing, overlap, card repetition, and mobile collapse.
- `adapt`: re-bias dials for another device, audience, density, register, or technical constraint.
- `clarify`: rewrite copy to remove filler, explain user control, and make CTAs and errors concrete.

## Hero Architectures

Choose one:

- Centered statement over full-bleed image.
- Bottom-left text over image with strong safe area.
- Editorial offset with text and media on asymmetric grid.
- Image-as-canvas with sparse UI overlays.
- Mini minimalist hero with abundant negative space.
- Product UI stack with one precise supporting claim.
- Inverted split: left media, right text.
- Classic text-left/image-right only when the brief truly needs it.

Hero rules:

- H1 should be short and strong.
- Keep first viewport uncluttered.
- Use one primary CTA and one optional secondary action.
- Let the hero establish the whole page's design system.

## Section Rhythm

Combine 4-8 sections with varied jobs:

- Hook: hero, product promise, immediate visual identity.
- Proof: logos, numbers, testimonials, press, case proof.
- Education: problem, mechanism, product walkthrough.
- Detail: bento feature cluster, comparison, pricing, FAQ.
- Emotion: image-led story, founder note, cultural cue, tactile moment.
- Conversion: final CTA, contact, checkout, booking, signup.

Vary scale across sections:

- One cinematic large section.
- One dense modular section.
- One quiet whitespace section.
- One image-led editorial section.
- One direct conversion section.

## Component Language

Pick 3-5 signature components:

- Restrained bento grid.
- Product UI panel stack.
- Large editorial image crop.
- Horizontal feature rail.
- Split testimonial wall.
- Oversized metric strip.
- Comparison matrix.
- Tactile material swatches.
- Sticky chapter navigation.
- Interactive product preview.
- Marquee only when brand inventory or social proof is real.

## Typography Characters

Pick one heading character and one body character:

- Swiss rational sans: precise, technical, trustworthy.
- Refined grotesk: premium SaaS, broad utility.
- Expressive display sans: studio, portfolio, creator brand.
- Editorial serif plus sans: culture, luxury, thought leadership.
- Condensed statement type: campaigns, sports, music, events.
- Humanist sans: wellness, education, local services.

Rules:

- Use variable fonts when available.
- Keep body text highly readable.
- Avoid more than two strong type personalities.
- Use type scale and spacing before decorative effects.

## Color And Material

Pick one palette mode:

- Pristine light: off-white, ink, one warm accent.
- Mature dark: graphite, soft elevation, desaturated accent.
- Bold studio: one strong brand field plus restrained neutrals.
- Tactile warm: paper, clay, textile, natural accent.
- Product technical: neutral surfaces, semantic color, precise accents.

Material options:

- Subtle noise texture.
- Soft translucent layer.
- Tonal gradient with low chroma.
- Duotone or color-graded image.
- Flat color block with product crop.
- Hairline grid or rule system.

Avoid one-note palettes and default AI purple-blue gradients unless explicitly brand-aligned.

## Image Direction

Images should carry structure, not fill empty space.

Use:

- Real product imagery or product UI screenshots.
- Editorial photography with clear crop logic.
- Full-bleed backgrounds with contrast overlays.
- Macro detail crops for material or product specificity.
- Generated bitmap visuals when real assets do not exist.

Avoid:

- Stock-like atmospheric images that do not reveal the product.
- Tiny decorative thumbnails.
- Random abstract art for functional interfaces.
- Image treatments that fight the palette.

## Prompt Pattern For Image Direction

Use this structure for design-reference image prompts:

```text
Create one horizontal website section design comp for [section job].
Brand/product: [specific product].
Audience: [audience].
Design thesis: [one sentence].
Hero/section architecture: [chosen architecture].
Typography: [heading/body character].
Palette/material: [palette and material].
Imagery: [image role and treatment].
Components: [specific components].
CTA priority: [primary/secondary].
Constraints: readable text, clear hierarchy, implementation-ready layout, no generic AI glow, no repeated card spam.
```

For full landing-page image direction, generate one separate horizontal comp per section and keep palette, typography, radius, image treatment, and CTA logic consistent across all sections.

## Motion Hero Prompt Pattern

Use this when asking an AI builder to implement a high-impact hero, inspired by MotionSites-style structure:

```text
Build a production-ready [stack] hero section for [product].
Goal: [conversion or brand effect].
Mood: [cinematic / liquid glass / editorial / product-first / technical premium].
Design tokens: define CSS variables for background, foreground, muted text, accent, surface, border, radius, shadow, and spacing.
Layout: [navbar structure], [hero grid or full-bleed architecture], [visual/media area], [CTA cluster], [proof row].
Typography: specify H1 size range, line-height, font weight, body size, label style, and responsive scaling.
Visual system: [image/video/3D/product UI], crop/framing, overlays, gradients, and material effects.
Motion: entrance sequence, hover states, background motion, scroll behavior, and prefers-reduced-motion fallback.
Components: buttons, badges, cards/media frames, logo/proof row, and interaction states.
Constraints: accessible contrast, mobile-first, no horizontal scroll, optimized media, no generic AI glow, no copied brand assets.
```

Keep the prompt specific enough to act like a design spec. Replace vague style words with measurable implementation choices whenever possible.
