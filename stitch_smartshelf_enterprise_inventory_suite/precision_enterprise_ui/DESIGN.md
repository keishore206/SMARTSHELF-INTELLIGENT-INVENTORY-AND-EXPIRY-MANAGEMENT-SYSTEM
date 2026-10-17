---
name: Precision Enterprise UI
colors:
  surface: '#f8f9ff'
  surface-dim: '#ccdbf3'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d5e3fc'
  on-surface: '#0d1c2e'
  on-surface-variant: '#434655'
  inverse-surface: '#233144'
  inverse-on-surface: '#eaf1ff'
  outline: '#747686'
  outline-variant: '#c4c5d7'
  surface-tint: '#2151da'
  primary: '#0037b0'
  on-primary: '#ffffff'
  primary-container: '#1d4ed8'
  on-primary-container: '#cad3ff'
  inverse-primary: '#b7c4ff'
  secondary: '#006a63'
  on-secondary: '#ffffff'
  secondary-container: '#99efe5'
  on-secondary-container: '#006f67'
  tertiary: '#3d445a'
  on-tertiary: '#ffffff'
  tertiary-container: '#545c72'
  on-tertiary-container: '#cdd5ef'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001551'
  on-primary-fixed-variant: '#0039b5'
  secondary-fixed: '#9cf2e8'
  secondary-fixed-dim: '#80d5cb'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#00504a'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#f8f9ff'
  on-background: '#0d1c2e'
  surface-variant: '#d5e3fc'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: -0.005em
  body-regular:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-medium:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  body-semibold:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  caption-regular:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  caption-medium:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  badge-label:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.05em
  tabular-data:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system targets mission-critical enterprise desktop workflows requiring deep data density, analytical clarity, and immediate comprehension. The visual ethos combines modern architectural restraint with high-efficiency utility: crisp 1px slate structural containment, rigorous tabular alignment, disciplined whitespace, and an absolute zero-emoji policy. 

The aesthetic is Modern Enterprise SaaS with an authoritative, technical precision. Surfaces feel physical, engineered, and reliable. Information density is prioritized without inducing cognitive fatigue by using a split structural canvas (deep obsidian slate control rail paired with an expansive, calibrated off-white workspace).

## Colors

The palette is engineered around high functional contrast and strict semantic clarity:

- **Primary Interactive (#1d4ed8):** High-efficiency Cobalt Royal Blue reserved for definitive forward actions, active navigation states, primary focus indicators, and key operational confirmations. Hover state deepens to `#1e40af`.
- **Secondary Interactive (#0f766e):** Slate Teal dedicated to analytical pathways, data exports, report generators, and secondary utility workflows.
- **Surface Infrastructure:**
  - Navigation Rail / Persistent Frame: Deep Obsidian Slate (`#0f172a`) framed with border strokes of `#1e293b`.
  - Main App Canvas: Subtle Slate Gray (`#f8fafc`).
  - Active Work Surfaces & Overlays: Crisp Pure White (`#ffffff`) bounded by precise 1px borders (`#e2e8f0`).
- **Typography Tiers:**
  - High Emphasis / Headings: Dark Slate (`#0f172a`) yielding a contrast ratio exceeding 12:1 against light canvas surfaces.
  - Standard Body: Balanced Slate (`#475569`).
  - Metadata & Muted Captions: Slate Gray (`#94a3b8`).
- **Status & Telemetry Tokens:**
  - Success / Active: Ink `#16a34a`, Background `#dcfce7`, Border `#bbf7d0`.
  - Warning / Attention: Ink `#d97706`, Background `#fef3c7`, Border `#fde68a`.
  - Danger / Terminal: Ink `#dc2626`, Background `#fee2e2`, Border `#fecaca`.
  - Neutral / Informational: Ink `#475569`, Background `#f1f5f9`, Border `#e2e8f0`.

## Typography

The type system is strictly structured around `Inter` for interface readability and contextual utility, augmented by monospaced styling for critical financial, volume, inventory, and telemetry numbers.

All numeric metric listings, table values, stock indicators, and timestamps must use tabular lining metrics or the designated monospaced token (`tabular-data`) to prevent vertical jitter during data sorting and real-time streaming updates. Letter spacing scales proportionally tighter on display headings to preserve line density and optical punch, while labels and micro-badges employ positive tracking to guarantee rapid scanability.

## Layout & Spacing

The layout utilizes a structured desktop-first shell architecture anchored to a 1440px primary viewport baseline, with responsive fluid adaptation:

- **Structural Architecture:** 
  - Persistent vertical navigation rail: fixed 260px width anchored to the left viewport boundary.
  - Main operational area: fills remaining width with fluid margins (`2rem` desktop down to `1rem` below 1024px).
  - Main content grid: 12-column layout with 24px (`1.5rem`) gutters. Content cards and analytical modules snap along 3, 4, 6, 8, or 12 column intervals.
- **Rhythm & Padding:** Strict 4px/8px modular scale. Dense data cells leverage `space-xs` and `space-sm`, interactive controls and cards use `space-md` to `space-lg`, and page sections expand into `space-xl`.

## Elevation & Depth

This system intentionally departs from heavily diffused drop shadows, utilizing low-contrast structural boundaries and subtle ambient floor-shadows:

- **Base Layer (Level 0):** Canvas backdrop (`#f8fafc`). Completely flat.
- **Surface Elevation (Level 1):** Main work cards, panels, and data grids sit directly above the canvas with a solid `#ffffff` fill, a crisp `1px solid #e2e8f0` outer perimeter, and an ultra-subtle grounding shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.05)`.
- **Raised Elevation (Level 2):** Context menus, popovers, and search dropdowns retain the 1px `#e2e8f0` border, enhanced by a directional elevation shadow: `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04)`.
- **Overlay Elevation (Level 3):** Modal windows and critical intervention dialogs present a sharp structural envelope (`1px solid #cbd5e1`) supported by high-spread stabilization: `0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.06)`, framed over an ambient backdrop scrim (`#0f172a` at 40% opacity).

## Shapes

The geometric framework is structured and precise. Base interactive elements (buttons, inputs, dropdown selectors) adhere to a clean 8px (`0.5rem`) radius, balancing modern softness with architectural alignment. 

- Interactive controls & containers: 8px border-radius (`roundedness: 2`).
- Nested interior items (segmented toggles, inner table highlights): 4px to 6px border-radius.
- Status, category, and telemetry badges: fully circular pill radius (9999px) to distinctly isolate classification tags from actionable button shapes.

## Components

### Buttons
- **Primary:** Background `#1d4ed8`, hover `#1e40af`, active `#172554`. Height 38px, horizontal padding `1rem`, border-radius 8px, font-weight 500, label color `#ffffff`.
- **Secondary (Analytical / Export):** Background `#0f766e`, hover `#115e59`, text `#ffffff`.
- **Outline / Neutral:** Background `#ffffff`, border `1px solid #e2e8f0`, text `#0f172a`, hover background `#f8fafc` and border `#cbd5e1`.
- **Icon Placement:** Accommodates monoline vector SVGs (16px to 20px) with 8px clearance to adjacent label text.

### Inputs & Selectors
- Height 38px, background `#ffffff`, border `1px solid #e2e8f0`, border-radius 8px, text `#0f172a`, placeholder text `#94a3b8`.
- **Focus State:** Border changes to `#1d4ed8` paired with an outer box-shadow ring: `0 0 0 3px rgba(29, 78, 216, 0.15)`.
- **Disabled State:** Background `#f1f5f9`, border `#e2e8f0`, text `#94a3b8`, cursor `not-allowed`.

### Badges & Status Indicators
- Height 22px, padding `2px 8px`, border-radius 9999px (pill-shaped), text transform uppercase, font-size 11px, weight 600, letter spacing `0.05em`.
- Normal / In Stock: Text `#16a34a`, background `#dcfce7`, border `1px solid #bbf7d0`.
- Warning / Low Stock: Text `#d97706`, background `#fef3c7`, border `1px solid #fde68a`.
- Danger / Critical: Text `#dc2626`, background `#fee2e2`, border `1px solid #fecaca`.
- Info / Neutral: Text `#475569`, background `#f1f5f9`, border `1px solid #e2e8f0`.

### Tables & Data Grids
- Header row: height 40px, background `#f8fafc`, text `#475569`, uppercase, font-size 12px, font-weight 600, border-bottom `1px solid #e2e8f0`.
- Data rows: height 48px, background `#ffffff`, text `#0f172a`, border-bottom `1px solid #f1f5f9`.
- Numeric content right-aligned using tabular monospace typography.
- Row hover state: background `#f8fafc`.

### Checkboxes & Radios
- Size 16px × 16px, border `1px solid #cbd5e1`, border-radius 4px (checkbox) or 50% (radio).
- Checked state: background `#1d4ed8`, border-color `#1d4ed8`, displaying a white 1.5px monoline check icon.

### Cards & Panels
- Background `#ffffff`, border `1px solid #e2e8f0`, border-radius 8px, box-shadow `0 1px 3px rgba(15, 23, 42, 0.05)`. Padding configured dynamically with `space-md` or `space-lg`.

### Iconography Rules
- Strict no-emoji enforcement. Use only monoline SVG vector glyphs (Lucide/Heroicons specification) sized strictly to 16px or 20px with a uniform 1.75px or 2px stroke width.