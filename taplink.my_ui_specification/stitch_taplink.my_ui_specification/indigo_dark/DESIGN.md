---
name: Indigo Dark
colors:
  surface: '#13131b'
  surface-dim: '#13131b'
  surface-bright: '#393841'
  surface-container-lowest: '#0d0d15'
  surface-container-low: '#1b1b23'
  surface-container: '#1f1f27'
  surface-container-high: '#292932'
  surface-container-highest: '#34343d'
  on-surface: '#e4e1ed'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e4e1ed'
  inverse-on-surface: '#303038'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#c0c1ff'
  on-secondary: '#292a60'
  secondary-container: '#42447b'
  on-secondary-container: '#b2b3f2'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#e1e0ff'
  secondary-fixed-dim: '#c0c1ff'
  on-secondary-fixed: '#13144a'
  on-secondary-fixed-variant: '#404178'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#13131b'
  on-background: '#e4e1ed'
  surface-variant: '#34343d'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.5'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 0.25rem
  sm: 0.5rem
  md: 1rem
  lg: 1.5rem
  xl: 2rem
  2xl: 3rem
  container-max: 640px
  gutter: 1rem
---

## Brand & Style
The design system is built for a high-performance, developer-centric aesthetic, specifically optimized for the link-in-bio and personal landing page space. The brand personality is **sophisticated, technical, and high-energy**, utilizing a deep dark-mode foundation contrasted against electric indigo accents.

The design style leans into **Modern Minimalism with subtle Glassmorphic influences**. It prioritizes extreme legibility and "clickability" through clear interactive states. The interface should feel like a premium command center—refined enough for professional portfolios, yet energetic enough for social media creators.

## Colors
The palette is centered on a "void" black base to ensure maximum contrast and energy efficiency on OLED screens. 

- **Primary Indigo** serves as the sole action color, used for high-intent buttons and active states.
- **Surface Layering** uses monochromatic steps from `#0a0a0a` to `#222222` to create depth without relying on heavy shadows.
- **Text Hierarchy** is strictly enforced: pure zinc whites for content, mid-grays for descriptions, and dark-grays for metadata.

## Typography
This design system utilizes **Inter** exclusively to maintain a systematic, utilitarian feel. 

- **Weight Usage**: Use Bold (700) for displays, SemiBold (600) for headlines and labels, and Regular (400) for all body text.
- **Tight Tracking**: Larger display sizes use negative letter-spacing to maintain a compact, modern appearance.
- **Scaling**: Headlines should aggressively scale down on mobile to ensure no word breaking on narrow devices.

## Layout & Spacing
The layout philosophy is **Mobile-First Fixed Grid**. Since the primary use case is a link-in-bio tool, content is centered in a single-column container with a maximum width of 640px.

- **Vertical Rhythm**: Use the `lg` (1.5rem) unit for spacing between distinct card elements.
- **Safe Areas**: Maintain a minimum `gutter` of 16px on mobile devices.
- **Desktop**: Content remains centered, utilizing the background color to frame the central experience.

## Elevation & Depth
Depth is conveyed through a combination of **Surface Toning** and **Strategic Glows**.

1.  **Z-Index 0 (Base)**: `#0a0a0a` — Used for the main page background.
2.  **Z-Index 1 (Surface)**: `#111111` — Used for main interactive cards.
3.  **Z-Index 2 (Elevated)**: `#1a1a1a` — Used for hover states or nested elements.
4.  **Shadows**: Use low-opacity black shadows for physical separation.
5.  **Brand Glow**: Apply a `0 0 20px rgba(99, 102, 241, 0.3)` shadow to primary buttons or featured "spotlight" cards to draw immediate user attention.

## Shapes
The shape language is **distinctly rounded** but not circular, providing a friendly feel to a tech-heavy aesthetic.

- **Cards**: Use `lg` or `xl` for the main content containers.
- **Buttons**: Use `md` for standard actions to maintain a precise, click-ready appearance.
- **Layout Groups**: Use `2xl` for decorative background sections or global containers.

## Components
Consistent implementation of components ensures a seamless user experience.

- **Primary Button**: Background: `primary_indigo`, Text: `white`. On hover, shift to `primary_hover` and apply the `brand glow`.
- **Secondary (Ghost) Button**: Background: `transparent`, Border: `border_default`, Text: `text_primary`. Hover: Background: `primary_subtle`, Border: `primary_indigo`.
- **Interactive Cards**: Background: `background_surface`, Border: `border_subtle`. On hover: Shift border to `border_default` and background to `background_elevated`. 
- **Alpine.js Patterns**: 
    - Use `x-data="{ hovered: false }"` on cards to trigger smooth border transitions.
    - Implement dropdowns or mobile menus using `x-show` with `transition:enter` and `transition:leave` set to 150ms ease-out.
- **Input Fields**: Background: `background_base`, Border: `border_subtle`. On focus: Border: `primary_indigo`, Ring: `brand glow` (inset).