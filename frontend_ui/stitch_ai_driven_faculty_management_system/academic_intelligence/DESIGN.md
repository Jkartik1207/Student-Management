---
name: Academic Intelligence
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#44474e'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#75777f'
  outline-variant: '#c5c6cf'
  surface-tint: '#4e5e81'
  primary: '#031635'
  on-primary: '#ffffff'
  primary-container: '#1a2b4b'
  on-primary-container: '#8293b8'
  inverse-primary: '#b6c6ef'
  secondary: '#4b41e1'
  on-secondary: '#ffffff'
  secondary-container: '#645efb'
  on-secondary-container: '#fffbff'
  tertiary: '#141819'
  on-tertiary: '#ffffff'
  tertiary-container: '#292c2e'
  on-tertiary-container: '#909395'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#b6c6ef'
  on-primary-fixed: '#081b3a'
  on-primary-fixed-variant: '#364768'
  secondary-fixed: '#e2dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#0f0069'
  on-secondary-fixed-variant: '#3323cc'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: Geist
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
---

## Brand & Style

This design system embodies "Modern Academic" excellence—a bridge between traditional institutional prestige and cutting-edge computational intelligence. The brand personality is authoritative yet accessible, designed to reduce the cognitive load of faculty members managing complex administrative and research tasks.

The visual style is **Corporate / Modern** with a focus on precision and clarity. It prioritizes high data density through disciplined whitespace management and a refined hierarchy. Every element is engineered to feel stable and reliable, while subtle motion and "AI-enhanced" visual cues provide a sense of forward-thinking innovation. The emotional response should be one of "effortless control" and "professional focus."

## Colors

The palette is anchored by **Deep Navy (#1A2B4B)**, representing the institutional foundation and professional trust. This color is used for primary navigation, headings, and high-level structural elements.

**AI Indigo (#4F46E5)** serves as the functional accent. It is reserved for interactive elements, primary actions, and "intelligent" states. When AI features are active, this color can expand into a subtle 10% opacity wash to highlight automated fields or insights.

The background system utilizes a "layered white" approach. The base canvas is **White (#FFFFFF)**, while **Slate Gray (#F8FAFC)** is used for secondary containers and dashboard backgrounds to provide subtle contrast and depth without introducing visual noise.

## Typography

This design system utilizes a dual-font approach to balance technical precision with readability. 

**Geist** is used for headlines, labels, and UI controls. Its monospaced-influenced geometry provides a "technical-academic" feel that remains highly legible at small sizes, making it ideal for data labels and dashboard headers.

**Inter** is the workhorse for all body copy and content-heavy areas. It is chosen for its neutral, systematic nature, ensuring that long-form research text or administrative reports are comfortable to read over long durations.

For mobile, scale down `headline-xl` and `headline-lg` by one tier to maintain balance. All body text should remain at its defined size to ensure accessibility for faculty members.

## Layout & Spacing

The layout utilizes a **12-column fluid grid** for desktop, optimized for data-heavy dashboards. On mobile, it collapses to a single-column view with 16px margins.

Spacing follows a strict **4px baseline grid**. Components should use `md` (16px) or `lg` (24px) padding to ensure high-density information remains scannable. Sections within a page should be separated by `2xl` (48px) to create clear mental breaks between different administrative tasks.

For data tables, use a "Compact" vertical rhythm (12px row padding) and a "Standard" rhythm (16px row padding) to allow users to customize their view based on their hardware and preference.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layering** and **Soft Ambient Shadows**. 

1. **Base Layer:** The light gray application background.
2. **Surface Layer:** White cards and containers, elevated by a very subtle 1px border (#E2E8F0).
3. **Elevated Layer:** Active cards or modals, which use a diffused shadow (0px 4px 12px rgba(26, 43, 75, 0.08)) to appear physically above the interface.

**AI Depth:** Special "AI-Insight" containers use a subtle, semi-transparent Indigo glow instead of a traditional shadow. This differentiates automated suggestions from static administrative data.

## Shapes

The design system employs a **Soft** shape language. Standard UI elements (buttons, inputs, cards) use a 4px (0.25rem) corner radius. This provides a professional, structured feel that aligns with institutional software while avoiding the harshness of sharp corners.

Larger containers and dashboard modules can scale up to 8px (0.5rem) to soften the overall appearance of complex layouts. Selection indicators and status badges use a "Pill" radius for immediate visual differentiation from functional buttons.

## Components

### Buttons
- **Primary:** Deep Navy background with white text. No shadow in rest state; subtle elevation on hover.
- **Secondary:** Transparent background with a 1px Navy border.
- **AI Action:** Indigo background with a subtle inner-glow effect to signal intelligence.

### Data Tables
- Header rows are Slate Gray (#F8FAFC) with uppercase Geist labels.
- Borders are restricted to horizontal lines only to reduce visual "caging."
- Row hover states use a light Indigo tint (#EEF2FF).

### Input Fields
- Subtle 1px Slate border.
- On focus, the border transitions to Indigo with a 2px soft outer glow.
- Error states use a muted red text with no background fill to maintain the clean aesthetic.

### Cards
- White background, 1px border (#E2E8F0).
- Titles should always use Geist Medium at 16px or 18px.
- Use internal padding of 24px (lg) for standard cards and 16px (md) for sidebar widgets.

### AI Status Indicators
- Use a small "sparkle" icon next to AI-generated fields.
- Backgrounds of AI-assisted text areas should have a faint linear gradient from White to a very pale Indigo (#F5F3FF).