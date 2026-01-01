---
name: atomic-component-architect
description: Guides the design of enterprise-grade clinical components using Atomic Design principles and Ant Design 5's Design Token system. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy for Next.js 15.
version: 1.1.0
dependencies:
  - antd>=5.0.0
  - "@ant-design/nextjs-registry>=1.0.0"
  - react>=19.0.0
---

# Atomic Component Architecture (Platform 1.0)

## Overview
High-compliance healthcare systems require "Bleeding Edge Stability"—advanced features (React 19/Next 15) coupled with enterprise-grade reliability. This skill enforces Atomic Design (Atoms, Molecules, Organisms, Templates) while leveraging Ant Design 5's dynamic CSS-in-JS and Design Token system to create dense, high-performance medical interfaces.

## When to Use
- Building new clinical UI primitives (StatusBadge, VitalsCard).
- Implementing global healthcare theming using the "Dense" algorithm.
- Optimizing bundle size and preventing "Flash of Unstyled Content" (FOUC) in Next.js 15 App Router.

## Core Hierarchy
- **Atoms**: Base elements (Buttons, Icons, Typography).
- **Molecules**: Simple groups of atoms (Search bar, Patient name field).
- **Organisms**: Complex dashboard sections (Sidebar, Medication schedule, Dense Tables).
- **Templates**: High-level page layouts arrangement using CSS Grid and Flexbox.

## Implementation Guidelines

### 1. Style Extraction & Hydration (Next.js 15 Registry)
To eliminate FOUC, always wrap clinical applications in the `AntdRegistry`. This extracts component styles during server-side rendering and injects them into the initial HTML payload.

```tsx
// app/layout.tsx
import { AntdRegistry } from '@ant-design/nextjs-registry';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AntdRegistry>{children}</AntdRegistry>
      </body>
    </html>
  );
}
```

### 2. Design Token System
Leverage the three-tier token hierarchy for clinical theming:
- **Seed Tokens**: Fundamental brand values (e.g., `colorPrimary`).
- **Map Tokens**: Derived states (e.g., `colorBorder`, `colorBgHover`).
- **Alias Tokens**: Semantic variables consumed by custom components (e.g., `token.colorTextSecondary`).

**Pattern**: Apply the `compact` algorithm to maximize data visibility for clinicians.

```tsx
// Use theme.useToken() hooks to build bespoke visualizations consistent with AntD.
const { token } = theme.useToken();
```

### 3. Tree-Shaking & Direct Path Imports
The App Router has limitations with dot-notation sub-components. To maintain efficient bundle sizes, import components directly.

```tsx
// ❌ Avoid: import { Typography } from 'antd'; <Typography.Title />
// ✅ Preferred: Direct export usage
import Title from 'antd/es/typography/Title';
```

## Anti-Patterns
- ❌ **Whitespace Excess**: Avoid default padding in clinical tables. Use the "Dense" theme algorithm.
- ❌ **FOUC**: Neglecting to use the `AntdRegistry` in a Next.js App Router environment.
- ❌ **Static CSS**: Hardcoding clinical colors instead of using the Design Token system via `useToken`.

## Real-World Example: Dense Medical Table Organism
An organism leveraging Ant Design 5's compact algorithm and path-specific imports for performance.

```tsx
"use client";
import Table from 'antd/es/table';
import { ConfigProvider, theme } from 'antd';

export const DenseVitalsTable = ({ data }) => {
  return (
    <ConfigProvider theme={{ algorithm: theme.compactAlgorithm }}>
       <Table 
         dataSource={data} 
         size="small" 
         pagination={false}
         bordered
       />
    </ConfigProvider>
  );
};
```
