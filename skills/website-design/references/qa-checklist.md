# QA Checklist

Use before finalizing a design, implementation, or critique.

## Concept

- The page has a clear design thesis.
- The register is explicit: `brand` for persuasion/identity or `product` for repeated-use utility.
- Design dials are stated and appropriate: visual ambition, information density, image reliance, motion level, conversion discipline, implementation clarity, and brand fidelity.
- The first viewport makes the brand/product obvious.
- The visual direction fits the audience and business model.
- Trends are used for function or identity, not decoration.
- External references are transformed into original design logic, not copied.
- The page does not look like a generic AI-generated SaaS template.

## Layout

- Clear scan order from headline to proof to CTA.
- Sections vary in density, alignment, and image-to-text ratio.
- No repeated same-shape card rows across the whole page.
- No incoherent overlap at desktop or mobile widths.
- Fixed-format elements use stable dimensions or aspect ratios.
- Mobile layout is not a squeezed desktop layout.

## Typography

- One H1 and logical heading hierarchy.
- Body text is readable at mobile sizes.
- Line lengths are controlled.
- Button and card text fits without cramped wrapping.
- Letter spacing is normal unless a display face needs careful adjustment.
- Type choices express brand without harming legibility.

## Color And Material

- Contrast is sufficient for body text, controls, and overlays.
- Palette has neutrals, primary, secondary/support, and accent roles.
- Dark mode surfaces use elevation and contrast, not simple inversion.
- Glass/translucency keeps text readable.
- Gradients are palette-matched and do not compete with content.

## Interaction

- Primary CTA is unmistakable.
- Controls have hover, focus, active, disabled, and loading states.
- Forms include labels above inputs, useful helper text where needed, and inline errors below the relevant field.
- Icon-only controls have accessible labels.
- Touch targets are at least 44px where practical.
- Motion communicates state or story and respects reduced motion.
- Motion prompt specs include timings, triggers, hover/press behavior, and fallback states.
- Navigation is discoverable and does not trap the user in scroll effects.

## Performance

- Hero media is optimized and sized.
- Below-fold images and heavy components lazy-load.
- Layout reserves image/media space to avoid shift.
- 3D/WebGL has fallback and does not block critical content.
- Fonts use limited families/weights and sensible loading.

## Content

- Copy is specific and believable.
- Avoid filler phrases: unleash, elevate, revolutionize, next-gen, seamless, powerful solution, transformative platform.
- Metrics and social proof are real or clearly placeholder during mockup.
- AI features explain what is generated, editable, reversible, or user-controlled.

## Deterministic Anti-Pattern Pass

Reject or revise before finalizing when any of these appear without a clear product reason:

- Generic AI SaaS signals: purple-blue glow gradients, floating orbs/blobs, centered hero plus generic dashboard mockup, or cloned text-left/image-right sections.
- Repeated equal-card grids, nested cards, same icon-heading-body blocks across multiple sections, or cards used where rules, tables, bands, screenshots, or negative space would be clearer.
- Decorative glass, blur, outer glow, mesh gradients, or shadows that reduce readability or do not express hierarchy.
- Fake precision: invented metrics, fake testimonials, generic names, generic company logos, or placeholder proof presented as real.
- Weak copy: filler value props, restated headings, vague AI claims, CTAs that do not state the action, or error/empty states with no recovery path.
- Product UI gaps: missing loading, empty, error, disabled, focus, active, long-text, small-screen, or reduced-motion states.
- Layout instability: `h-screen` heroes that can jump on mobile, text containers without wrapping strategy, media without reserved dimensions, horizontal scroll, or buttons whose labels overflow.
- Motion/performance risks: animating layout properties, scroll listeners without cleanup, perpetual animation outside isolated client components, or no fallback for heavy 3D/WebGL.

## Register-Specific Pass

- `brand`: first viewport has a memorable concept, strong CTA path, real visual media or product signal, varied section rhythm, and no generic startup language.
- `product`: screen supports fast scanning, keyboard/focus behavior, dense but calm information layout, semantic color, useful states, and low-friction repeated action.
- Mixed pages: marketing sections may be expressive, but working UI screenshots and product surfaces must remain legible, stable, and believable.

## Code Review Focus

When reviewing implementation, inspect:

- CSS color and spacing tokens.
- Responsive breakpoints.
- Accessibility labels and focus styles.
- Animation implementation and reduced-motion behavior.
- Image dimensions, formats, and loading attributes.
- Repeated component abstractions that cause visual sameness.
