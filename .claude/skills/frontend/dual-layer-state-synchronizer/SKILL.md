---
name: dual-layer-state-synchronizer
description: Synchronizes Server State (React Query 5) and Client State (Zustand 4.5) while maintaining URL as the single source of truth using nuqs. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - "@tanstack/react-query>=5.56.0"
  - zustand>=4.5.5
  - nuqs>=1.0.0
  - ably>=1.2.0
---

# Dual-Layer State Synchronization (Platform 1.0)

## Overview
Differentiates between "Server State" (clinical data in the HIMS database) and "Client State" (UI preferences and toggles). Employs React Query 5 for robust caching and Zustand 4.5 for lightweight client-side state, ensuring clinician efficiency and data sovereignty.

## When to Use
- Prefetching clinical records on the server to reduce Time to First Meaningful Paint.
- Managing user-specific UI preferences (e.g., sidebar state, theme mode).
- Implementing sharable clinical views via bookmarked URL filters.
- Real-time synchronization of lab values or emergency alerts via WebSockets.

## Domain Synchronization Patterns

### 1. Server State: Hydration/Dehydration Pattern
Utilize React Query 5 to prefetch data on the server within a Server Component, then "dehydrate" it for the client.

```tsx
// app/ward/page.tsx
const queryClient = getQueryClient();
await queryClient.prefetchQuery({ 
  queryKey: ['ward', wardId], 
  queryFn: () => fetchWardData(wardId) 
});

return (
  <HydrationBoundary state={dehydrate(queryClient)}>
    <WardDashboard wardId={wardId} />
  </HydrationBoundary>
);
```
**Rule**: Always use the object-based syntax for `useQuery` and centralize clinical keys in a factory function.

### 2. Client State: Request-Scoped Stores
**CRITICAL**: Avoid global variable stores on the server to prevent PII leakage between user requests. Always create Zustand stores per-request via a React Context provider.

```tsx
// lib/store/UIStoreProvider.tsx
export const UIStoreProvider = ({ children }) => {
  const storeRef = useRef(createUIStore()); // Scoped to this lifecycle
  return <UIContext.Provider value={storeRef.current}>{children}</UIContext.Provider>;
};
```

### 3. Real-time "Poke/Pull" Synchronization
Integrate Ably WebSockets with React Query for low-latency updates without overloading the client.
- **Poke**: Server sends a lightweight signal via Ably.
- **Pull**: Client triggers `queryClient.invalidateQueries` to fetch fresh clinical data via REST.

### 4. URL as Source of Truth (`nuqs`)
Treat the URL as the deterministic state for diagnostic dashboards.

```tsx
import { useQueryState } from 'nuqs';
// Filter list of patients by severity
const [severity, setSeverity] = useQueryState('severity');
```

## State Management Matrix

| Domain | Tool | Characteristic | Benefit |
| :--- | :--- | :--- | :--- |
| Server Data | React Query 5 | Hydrated Cache | Background sync, retry logic. |
| UI Preferences | Zustand 4.5 | Local Store | High-performance re-renders. |
| Active Filters | nuqs | URL Params | Bookmarkable clinical views. |

## Anti-Patterns
- ❌ **Global Module Stores**: Defining Zustand stores as module-level globals on the server (Data Sovereignty violation).
- ❌ **PII in Global State**: Storing identifiable patient data in a client store not scoped to the request.
- ❌ **Manual Sync Boilerplate**: Using `useEffect` to sync WebSockets to local state instead of the "Poke/Pull" pattern.
