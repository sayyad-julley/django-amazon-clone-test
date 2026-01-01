---
name: isomorphic-layout-orchestrator
description: Orchestrates Next.js 15 App Router layouts using Server Components (RSC), Parallel Routes, and Intercepted Routes for high-density clinical dashboards. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - next>=15.0.0
  - react>=19.0.0
---

# Isomorphic Layout Orchestration (Platform 1.0)

## Overview
Guides the creation of high-performance healthcare layouts that prioritize clinical state preservation and situational awareness. Leverages Next.js 15 Parallel and Intercepted Routes to partition the UI into discrete functional slots, ensuring that a failure in one module (e.g., latency in a DICOM server) does not degrade the entire dashboard.

## When to Use
- Designing multi-slot clinical dashboards (e.g., `@vitals`, `@orders`, `@reports`, `@analytics`).
- Implementing non-disruptive patient drill-downs (e.g., viewing lab results or allergy history) using Intercepted Routes.
- Optimizing initial page load by shifting data-intensive operations to the server via RSC.

## Core Patterns

### 1. Parallel Route & Granular Slot Management
Use named slots (`@folder`) to render multiple independent regions. Each slot should act as a mini-application with its own boundaries.

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  vitals,
  reports,
  analytics
}: {
  children: React.ReactNode;
  vitals: React.ReactNode;
  reports: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-12">{children}</div>
      <div className="col-span-4">{vitals}</div>
      <div className="col-span-5">{reports}</div>
      <div className="col-span-3">{analytics}</div>
    </div>
  );
}
```

### 2. Context-Preserving Modals (Intercepted Routes)
Use relative segment markers to overlay views without full-page transitions. This paradigm maintains the physician's context while allowing deep-linking.

| Marker | Meaning | Dashboard Use Case |
| :--- | :--- | :--- |
| `(.)folder` | Intercept same level | Opening a prescription edit form without navigating away from the history. |
| `(..)folder` | Intercept parent | Viewing patient details from a ward-level list view. |
| `(...)folder`| Intercept root | Global search results overlaying any dashboard segment. |

### 3. Critical Fallbacks & Resilience
- **`default.tsx`**: ALWAYS provide a `default.tsx` for every slot to prevent 404 errors during hard browser refreshes if the slot does not match the current URL.
- **Granular Feedback**: Use per-slot `loading.tsx` and `error.tsx` to ensure that slow connections to specific clinical services display local indicators rather than blocking the main UI thread.

## Anti-Patterns
- ❌ **SPA Heavy Lift**: Avoid putting all state logic in top-level client components. Use RSC for server-side clinical data fetching.
- ❌ **Missing Loading Slots**: Don't skip `loading.tsx` for parallel slots; it leads to jarring layout shifts in multi-panel dashboards.
- ❌ **Hard Refresh Dead-ends**: Forgetting `default.tsx` in parallel routes, which causes the entire layout to break on manual reloads.

## Real-World Example: Clinical Workbench
A workbench showing a patient list (Children), real-time vitals (`@vitals`), and an intercepted prescription modal.

```bash
# Structure
app/dashboard/
  layout.tsx
  page.tsx (Patient List)
  @vitals/
    page.tsx
    loading.tsx   # Local vital signs loading
    error.tsx     # Graceful failure if Vitals API is down
  @modals/
    (.)prescription/[id]/page.tsx
    default.tsx   # Critical fallback
```
