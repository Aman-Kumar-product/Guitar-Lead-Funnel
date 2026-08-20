---
name: Luminous Technical Dark
colors:
  surface: '#0f1513'
  surface-dim: '#0f1513'
  surface-bright: '#343a39'
  surface-container-lowest: '#090f0e'
  surface-container-low: '#171d1c'
  surface-container: '#1b2120'
  surface-container-high: '#252b2a'
  surface-container-highest: '#303635'
  on-surface: '#dee4e1'
  on-surface-variant: '#b9cbbd'
  inverse-surface: '#dee4e1'
  inverse-on-surface: '#2b3230'
  outline: '#849588'
  outline-variant: '#3b4a40'
  surface-tint: '#00e293'
  primary: '#cdffde'
  on-primary: '#003921'
  primary-container: '#00f5a0'
  on-primary-container: '#006b43'
  inverse-primary: '#006c44'
  secondary: '#ffb956'
  on-secondary: '#452b00'
  secondary-container: '#c58311'
  on-secondary-container: '#3d2500'
  tertiary: '#e4f8f2'
  on-tertiary: '#233430'
  tertiary-container: '#c8dbd6'
  on-tertiary-container: '#4f615d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#50ffaf'
  primary-fixed-dim: '#00e293'
  on-primary-fixed: '#002111'
  on-primary-fixed-variant: '#005232'
  secondary-fixed: '#ffddb5'
  secondary-fixed-dim: '#ffb956'
  on-secondary-fixed: '#2a1800'
  on-secondary-fixed-variant: '#633f00'
  tertiary-fixed: '#d3e7e1'
  tertiary-fixed-dim: '#b7cbc5'
  on-tertiary-fixed: '#0e1f1c'
  on-tertiary-fixed-variant: '#394a46'
  background: '#0f1513'
  on-background: '#dee4e1'
  surface-variant: '#303635'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 64px
    fontWeight: '900'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Montserrat
    fontSize: 36px
    fontWeight: '900'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-padding-desktop: 48px
  container-padding-mobile: 20px
  gutter: 24px
  section-gap: 80px
---

## Brand & Style

This design system is built on a foundation of **High-Contrast Dark** aesthetics mixed with **Glassmorphism** and **Tactile** lighting. It is designed for premium, technology-driven experiences that require an immersive, "always-on" dashboard feel.

The brand personality is authoritative yet energetic, utilizing deep charcoal foundations to let vibrant, neon-inflected accents "pop" with artificial light. It evokes a sense of forward-thinking precision and exclusivity. Visual depth is achieved not through traditional drop shadows, but through internal glows, outer radials, and subtle border gradients that simulate self-illuminated hardware interfaces.

## Colors

The palette is optimized for OLED and high-resolution displays, prioritizing deep black-greens and charcoals to reduce eye strain while maximizing the impact of functional color.

- **Primary (Neon Green):** Used for primary actions, success states, and "active" status indicators. It should frequently be paired with a matching outer glow (bloom effect).
- **Secondary (Warm Orange):** Used for highlighting key information, warning states, and distinct CTA variations to prevent visual monotony.
- **Surface & Backgrounds:** The main background is a near-black charcoal (`#050A09`). Component containers use a slightly lighter, desaturated teal-black (`#0B1412`) to create a discernible layered hierarchy.
- **Accents:** Use low-opacity versions of the primary green for subtle borders and container backgrounds to simulate glass-like transparency over the dark void.

## Typography

The typographic system balances high-impact geometric headers with ultra-readable, contemporary body text.

- **Headlines:** Use **Montserrat** for its bold, architectural presence. In large display formats, use tight letter-spacing and capitalize key terms to mimic the "future-tech" aesthetic seen in the reference.
- **Body:** **Be Vietnam Pro** provides a warm, approachable contrast to the sharp headers, ensuring long-form content remains legible against dark backgrounds.
- **Technical Labels:** **Space Grotesk** is used for "meta" information (e.g., tags, step indicators, button labels) to reinforce the technical, data-driven nature of the interface.
- **Gradient Text:** Use linear gradients (Primary Green to Secondary Orange) sparingly on major headlines to emphasize key narrative shifts.

## Layout & Spacing

The layout follows a **Fluid Grid** model with generous vertical breathing room to maintain a "premium" feel. 

- **Grid:** A 12-column system for desktop, collapsing to 4 columns on mobile. 
- **Rhythm:** All spacing is based on an 8px baseline. Use larger gaps (`section-gap`) between thematic blocks to allow the "glow" of containers to occupy space without feeling cluttered.
- **Safe Areas:** Cards should always have a minimum internal padding of 32px on desktop to ensure content doesn't feel cramped against the illuminated borders.

## Elevation & Depth

This design system eschews traditional shadows in favor of **Luminous Layering**.

1. **Level 0 (Background):** Deepest black. Often features a subtle noise texture or a very faint radial gradient in the center to suggest a light source behind the UI.
2. **Level 1 (Containers):** Soft, rounded cards with a 1px stroke. The stroke should be a low-opacity version of the primary color or a subtle gradient. 
3. **Level 2 (Interactive):** Elements that "float" above Level 1 use "Bloom Shadows"—high-diffusion, colored glows (e.g., a green glow under a green button) that suggest the element is a physical light source.
4. **Glassmorphism:** Use a `backdrop-filter: blur(12px)` on modal overlays or sticky navigation bars to maintain the immersive depth of the background while providing legibility.

## Shapes

The shape language is consistently **Rounded**. 

- **Main Containers:** Use a 1rem (16px) radius to soften the high-contrast technical aesthetic, making it feel modern rather than aggressive.
- **Buttons & Chips:** Use fully pill-shaped (rounded-full) corners for primary CTAs to make them feel tactile and "clickable."
- **Icons:** Should be housed in rounded-square enclosures with a 12px radius, featuring a subtle inner-glow to match the container style.

## Components

### Buttons
- **Primary:** Gradient fill (Primary Green to a slightly yellower green), pill-shaped, with a 15px blurred bloom shadow of the same color. Text is high-contrast black.
- **Secondary:** Transparent background with a 1.5px solid border in Secondary Orange. Subtle orange glow on hover.

### Cards
- Background: `#0B1412` at 80% opacity with backdrop-blur.
- Border: 1px solid `#1A2C29`.
- Feature: Cards should include a "top-light"—a very thin, 2px highlight at the very top edge of the card to simulate overhead lighting.

### Input Fields
- Dark, recessed backgrounds with bottom-only borders that "light up" (change color to Primary Green) when focused. 
- Placeholder text should be low-contrast (40% opacity white).

### Chips & Tags
- Small, uppercase labels with a high-contrast background and a "dot" icon representing status. Use the Secondary Orange for "Coming Soon" or "New" features.

### Progress Indicators
- Use segmented bars with rounded caps. The "active" segments should have a neon glow, while inactive segments are dark grey.