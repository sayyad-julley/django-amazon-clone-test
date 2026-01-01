---
name: css-layer-stylist
description: Orchestrates CSS specificity between Tailwind CSS 3 and Ant Design 5 using CSS Cascading Layers and StyleProvider. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - tailwindcss>=3.0.0
  - antd>=5.0.0
  - "@ant-design/cssinjs>=1.0.0"
---

# CSS Layer Styling (Platform 1.0)

## Overview
High-reliability medical UIs require sophisticated specificity management to prevent conflicting styles. This skill integrates Tailwind CSS 3 (utility-first) with Ant Design 5 (CSS-in-JS) using CSS Cascading Layers (`@layer`) to explicitly lower library specificity below utility classes.

## When to Use
- Implementing custom clinical UI patterns that require Tailwind overrides for AntD components.
- Resolving conflicts between library resets and custom healthcare branding.
- Managing specificity in dense multi-panel medical dashboards.

## Implementation Workflow

### 1. Specificity Management (@layer)
Define the layer order in your global CSS to ensure Tailwind utilities always win over library-internal styles.

```css
/* global.css */
@layer tailwind-base, antd;

@layer tailwind-base {
  @tailwind base;
}
@tailwind components;
@tailwind utilities;
```

### 2. Style Encapsulation (StyleProvider)
Configure Ant Design's `StyleProvider` from `@ant-design/cssinjs` to encapsulate the library's styles within the named `antd` layer. This lowers the priority of library selectors (which often use the `:where` selector).

```tsx
import { StyleProvider } from '@ant-design/cssinjs';

export default function ClinicalApp({ children }) {
  return (
    <StyleProvider layer="antd">
      {children}
    </StyleProvider>
  );
}
```

### 3. Component Abstraction vs. "Class Soup"
To prevent unmanageable class strings in clinical HTML, encapsulate repetitive patterns into reusable React components.
- Use **Tailwind utilities** for responsive layouts and micro-adjustments.
- Use **Ant Design Tokens** for brand-consistent theming (colors, borders).
- Use **@apply** sparingly and only for truly repetitive patterns to minimize CSS bundle size.

## Anti-Patterns
- ❌ **Specificity Wars**: Using `!important` to force overrides instead of relying on the `@layer` hierarchy.
- ❌ **FOUC**: Neglecting `AntdRegistry` in Next.js 15, causing flickering during initial clinical data loads.
- ❌ **Class Soup**: Allowing nested div structures to proliferate with long Tailwind class strings; abstract into Atoms/Molecules.

## Real-World Example: Urgent Medical Alert
Overriding an AntD Alert background with Tailwind's specific urgency colors while maintaining the library's enterprise icons and padding.

```tsx
// ClinicalAlert.tsx
import Alert from 'antd/es/alert';

export const UrgentAlert = ({ message }) => (
  <Alert 
    message={message} 
    type="error" 
    showIcon
    className="!bg-red-600 !text-white border-none shadow-lg" 
  />
);
```
