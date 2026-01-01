---
name: performance-first-optimizer
description: Optimizes high-density clinical dashboards for Time to Interactive (TTI) and First Contentful Paint (FCP). Aligned with Platform 1.0 "Performance First" strategy for point-of-care readiness.
version: 1.1.0
dependencies:
  - next>=15.0.0
  - react>=19.0.0
---

# Performance-First Optimization (Platform 1.0)

## Overview
The "Performance First" strategy ensures clinical workstations remain responsive and ready at the point of care. This skill focuses on minimizing the JavaScript payload, managing dense data rendering, and eliminating hydration discrepancies in high-compliance healthcare environments.

## When to Use
- Loading secondary clinical modules (e.g., medical imaging viewers or billing calculators) on-demand.
- Rendering dense patient lists or ward views without locking the UI thread.
- Resolving hydration mismatches between server-rendered clinical data and client-side updates.

## Optimization Patterns

### 1. Granular Code Splitting (`next/dynamic`)
Next.js 15 handles page-level splitting, but dense dashboards require component-level control. Load heavyweight dependencies only when the clinician interacts with them.

```tsx
import dynamic from 'next/dynamic';

const ImagingViewer = dynamic(() => import('./ImagingViewer'), {
  loading: () => <Skeleton active />,
  ssr: false, // For browser-only DICOM shaders or canvas
});
```

### 2. Intersection-Based Rendering
Improve performance for departments with high patient throughput by delaying the rendering of patient cards that are currently below the fold.

```tsx
// Delay fetching and rendering of dense records using a useOnScreen hook
const isVisible = useOnScreen(recordRef);

return (
  <div ref={recordRef}>
    {isVisible ? <DensePatientCard data={patient} /> : <Placeholder />}
  </div>
);
```

### 3. Eliminating Hydration Errors
Platform 1.0 requires strict handling of discrepancies between server and client renders to prevent UI flickering.
- **Environmental Discrepancies**: Never access `window` or `localStorage` during initial render.
- **Temporal Values**: Use `useEffect` to display relative timestamps (e.g., "Last updated 2s ago") after hydration.
- **Deterministic Data**: Use `useEffect` or `suppressHydrationWarning` for unavoidable locale or extension differences.

### 4. Isomorphic Processing
Shift data-intensive operations (parsing massive FHIR payloads) to the server using React Server Components (RSC) to minimize the client-side CPU burden.

## Anti-Patterns
- ❌ **Massive Global Bundles**: Avoid importing large medical visualization libraries in the root layout or common providers.
- ❌ **Client-Side Heavy Parsing**: Don't parse raw diagnostic results on the client; transform them into lean UI view models on the server.
- ❌ **Eager Loading secondary tabs**: Don't load the JavaScript for the "Insurance Billing" tab while the clinician is viewing the "Vital Signs" dashboard.

## Real-World Example: High-Throughput Ward View
The dashboard displays the top 10 high-risk patients instantly using RSC. As the clinician scrolls, the `Intersection Observer` triggers the dynamic loading of detailed lab result modules for patients currently on screen.
