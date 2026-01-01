---
dependencies:
- algoliasearch>=5.45.0
- react-instantsearch>=7.20.0
- react-instantsearch-nextjs>=1.0.3
- next>=15.0.0
- react>=19.0.0
description: Implements Algolia v5 search with Next.js 15 App Router and React 19
  by applying proven patterns (lite client singleton, async searchParams with await,
  client component composition, Suspense boundaries), following best practices (React
  19 peer dependency overrides, hydration mismatch prevention, URL synchronization),
  implementing workarounds (package.json overrides, suppressHydrationWarning, debounced
  routing), and avoiding anti-patterns (phantom React 18 dependencies, server-side
  indexing leaks, dynamic rendering conflicts, client re-initialization). Use when
  building Next.js 15 search, migrating from Pages Router, handling React 19 peer
  dependency conflicts, implementing SSR search with async params, or avoiding hydration
  mismatches.
name: implementing-algolia-nextjs15-react19
version: 1.0.0
---

# Implementing Algolia Next.js 15 + React 19

## Overview

Integrates Algolia v5 (5.45.0), react-instantsearch 7.20.0, and react-instantsearch-nextjs 1.0.3 with Next.js 15 App Router and React 19. The version triad introduces architectural shifts: async request APIs, strict hydration enforcement, and modular client architecture. Focus: Production patterns, peer dependency resolution, hydration safety, and SSR compatibility.

## When to Use

Use this skill when:
- Building Next.js 15 search with Algolia v5
- Migrating from Pages Router (getServerState) to App Router
- Handling React 19 peer dependency conflicts with Radix UI/shadcn
- Implementing SSR search with async searchParams
- Avoiding hydration mismatches in React 19 strict mode
- Resolving "Invalid Hook Call" errors from nested React versions

**Input format**: Next.js 15+ project with App Router, React 19, TypeScript configuration, Algolia account with API keys

**Expected output**: Production-ready Algolia search implementation following patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

- Next.js 15+ with App Router
- React 19 installed (or RC during transition)
- Algolia account with Search-Only and Admin API keys
- TypeScript configuration with strict mode
- Understanding of async/await patterns

## Core Patterns

### Pattern 1: Lite Client Initialization

Algolia v5 introduces `liteClient` for search-only operations, excluding heavy indexing logic. Use singleton pattern to prevent re-initialization.

**Template**:
```typescript
'use client';
import { useMemo } from 'react';
import { liteClient as algoliasearch } from 'algoliasearch/lite';

const APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || '';
const API_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY || '';

export function Search() {
  const searchClient = useMemo(
    () => algoliasearch(APP_ID, API_KEY),
    []
  );
  return <InstantSearchNext searchClient={searchClient} />;
}
```

**Best Practice**: Initialize outside component or use `useMemo` with empty dependency array for referential stability.

**Anti-Pattern**: Re-initializing client in render body causes infinite loops and stalled searches.

### Pattern 2: Async searchParams Handling

Next.js 15 makes `searchParams` a Promise. Access requires async page component and await.

**Template**:
```typescript
interface PageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export const dynamic = 'force-dynamic';

export default async function SearchPage({ searchParams }: PageProps) {
  await searchParams; // Mandatory in Next.js 15
  return (
    <Suspense fallback={<SearchSkeleton />}>
      <Search />
    </Suspense>
  );
}
```

**Best Practice**: Force dynamic rendering with `export const dynamic = 'force-dynamic'` to prevent static generation failures.

**Anti-Pattern**: Synchronous access to `searchParams.q` causes runtime errors or build-time type errors.

### Pattern 3: Client Component Composition

Maintain server/client boundary. Create separate Search component (use client) imported into server page.

**Template**:
```typescript
// app/search/Search.tsx
'use client';
import { InstantSearchNext } from 'react-instantsearch-nextjs';

export function Search() {
  // Client component logic
}

// app/search/page.tsx
import { Suspense } from 'react';
import { Search } from './Search';

export default async function Page({ searchParams }: PageProps) {
  await searchParams;
  return <Suspense><Search /></Suspense>;
}
```

**Best Practice**: Keep page.tsx as Server Component to use server-only features (generateMetadata, database calls).

**Anti-Pattern**: Making entire page client-side prevents using server-only features.

### Pattern 4: Suspense Boundary Requirement

Wrap InstantSearchNext in Suspense to prevent full-page client-side bailout.

**Template**:
```typescript
export default async function Page({ searchParams }: PageProps) {
  await searchParams;
  return (
    <div>
      <header>Static Server Content</header>
      <Suspense fallback={<SearchSkeleton />}>
        <Search />
      </Suspense>
    </div>
  );
}
```

**Best Practice**: Suspense allows Next.js to send static shell (header, footer) immediately while search streams.

**Anti-Pattern**: Missing Suspense causes entire page to switch to client-side rendering, defeating SEO.

## Best Practices

### Workaround 1: React 19 Peer Dependency Resolution

Radix UI and other libraries declare `react@^18.0` peer dependency, causing conflicts with Next.js 15 (React 19).

**Template**:
```json
{
  "overrides": {
    "react": "$react",
    "react-dom": "$react-dom",
    "@types/react": "$react",
    "@types/react-dom": "$react-dom"
  }
}
```

**Mechanism**: Force React 19 resolution for all packages. React 19 maintains backward compatibility with React 18 API.

**Alternative**: Use `npm install --legacy-peer-deps` (not recommended for production).

### Workaround 2: Hydration Mismatch Prevention

React 19 strict hydration flags dynamic content differences. Use `suppressHydrationWarning` or `useEffect` for client-only rendering.

**Template**:
```typescript
// For dynamic timestamps or relative dates
<div suppressHydrationWarning>
  {new Date().toLocaleString()}
</div>

// Or use useEffect for client-only rendering
'use client';
import { useEffect, useState } from 'react';

export function DynamicContent() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  return <div>{Date.now()}</div>;
}
```

**Mechanism**: `suppressHydrationWarning` tells React to ignore differences on specific elements. `useEffect` ensures client-only rendering after mount.

**Rationale**: React 19 strict hydration prevents "Extension Problem" (browser extensions injecting attributes) and timestamp mismatches.

### Workaround 3: URL Synchronization

Configure react-instantsearch-nextjs routing to debounce URL updates and prevent excessive history stack.

**Template**:
```typescript
<InstantSearchNext
  routing={{
    router: {
      windowTitle: (routeState) => `Search: ${routeState.query}`,
    }
  }}
  indexName="products"
  searchClient={searchClient}
>
  {/* Search components */}
</InstantSearchNext>
```

**Mechanism**: Built-in router adapter hooks into `next/navigation` and debounces URL updates during typing.

**Rationale**: Prevents history stack pollution and improves performance.

## Anti-Patterns

### Anti-Pattern 1: Phantom React 18 Dependency

**Symptom**: "Invalid Hook Call" or "Dispatcher is null" errors at runtime.

**Cause**: Nested `react@18` in `node_modules` from transitive dependencies (date pickers, carousels). Package manager installs both React 19 (root) and React 18 (nested).

**Remediation**:
```bash
npm dedupe
# Or in package.json
"overrides": {
  "react": "$react",
  "react-dom": "$react-dom"
}
```

**Prevention**: Use strict overrides in package.json and verify single React version with `npm ls react`.

### Anti-Pattern 2: Server-Side Indexing Leak

**Symptom**: Admin API key appears in client bundle, exposed in browser DevTools.

**Cause**: Importing full `algoliasearch` client (includes indexing logic) in UI components. Bundler includes Admin key even if code isn't executed.

**Remediation**: Strict separation:
- **UI Components**: Use `algoliasearch/lite` (search-only)
- **API Routes**: Use full `algoliasearch` for indexing (server-only)

**Template**:
```typescript
// app/api/reindex/route.ts (Server-only)
import algoliasearch from 'algoliasearch';
const client = algoliasearch(APP_ID, ADMIN_KEY); // Safe on server

// app/search/Search.tsx (Client component)
import { liteClient as algoliasearch } from 'algoliasearch/lite';
const client = algoliasearch(APP_ID, SEARCH_KEY); // Lite client
```

### Anti-Pattern 3: Dynamic Rendering Conflicts

**Symptom**: Search page works in development (`next dev`) but breaks in production with 404s or 500s.

**Cause**: Missing `export const dynamic = 'force-dynamic'`. Next.js attempts static generation without query parameters, causing build failures.

**Remediation**: Always add `export const dynamic = 'force-dynamic'` to search pages.

**Template**:
```typescript
export const dynamic = 'force-dynamic';

export default async function SearchPage({ searchParams }: PageProps) {
  await searchParams;
  // ...
}
```

### Anti-Pattern 4: Client Re-initialization

**Symptom**: Infinite loops of network requests, stalled search states, client reset before results return.

**Cause**: Creating Algolia client inside component render body. React 19 concurrent rendering and strict effect execution cause re-initialization on every render.

**Remediation**: Use singleton pattern (initialize outside component) or `useMemo` with empty dependency array.

**Template**:
```typescript
// ✅ Good: Singleton
const searchClient = algoliasearch(APP_ID, API_KEY);

// ✅ Good: useMemo
const searchClient = useMemo(() => algoliasearch(APP_ID, API_KEY), []);

// ❌ Bad: Re-initializes on every render
function Search() {
  const client = algoliasearch(APP_ID, API_KEY); // Don't do this
}
```

## Code Templates

### Template 1: Complete Client Component

```typescript
'use client';
import { useMemo } from 'react';
import { liteClient as algoliasearch } from 'algoliasearch/lite';
import { InstantSearchNext } from 'react-instantsearch-nextjs';
import { SearchBox, Hits, RefinementList } from 'react-instantsearch';

const APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || '';
const API_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY || '';

export function Search() {
  const searchClient = useMemo(
    () => algoliasearch(APP_ID, API_KEY),
    []
  );

  return (
    <InstantSearchNext
      indexName="products"
      searchClient={searchClient}
      routing={true}
      future={{ preserveSharedStateOnUnmount: true }}
    >
      <SearchBox />
      <RefinementList attribute="brand" />
      <Hits />
    </InstantSearchNext>
  );
}
```

### Template 2: Async Page Wrapper

```typescript
import { Suspense } from 'react';
import { Search } from './Search';

interface PageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export const dynamic = 'force-dynamic';

export default async function SearchPage({ searchParams }: PageProps) {
  await searchParams;
  return (
    <Suspense fallback={<SearchSkeleton />}>
      <Search />
    </Suspense>
  );
}
```

### Template 3: Package.json Overrides

```json
{
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "algoliasearch": "^5.45.0",
    "react-instantsearch": "^7.20.0",
    "react-instantsearch-nextjs": "^1.0.3"
  },
  "overrides": {
    "react": "$react",
    "react-dom": "$react-dom",
    "@types/react": "$react",
    "@types/react-dom": "$react-dom"
  }
}
```

## Error Handling

**Peer Dependency Conflicts**:
- Symptom: `npm install` fails with peer dependency warnings
- Resolution: Add `overrides` in package.json (see Template 3)
- Verification: Run `npm ls react` to confirm single React version

**Hydration Mismatches**:
- Symptom: React 19 hydration errors in console, full page re-render
- Resolution: Use `suppressHydrationWarning` or `useEffect` for dynamic content
- Prevention: Avoid `Date.now()`, `Math.random()`, or non-deterministic data in initial render

**Build Failures in CI/CD**:
- Symptom: Build works locally but fails in CI
- Resolution: Ensure `overrides` in package.json, verify `node_modules` aren't cached with wrong versions
- Prevention: Use `npm ci` in CI to ensure clean install

**Runtime Errors from Client Re-initialization**:
- Symptom: Infinite loops, stalled searches, "client is reset" errors
- Resolution: Move client initialization outside component or use `useMemo`
- Verification: Check React DevTools for component re-render frequency

## Security Guidelines

**CRITICAL**: Never hardcode sensitive information:
- ❌ No Admin API keys in frontend code
- ❌ No API keys in SKILL.md or example code
- ❌ No credentials in version control
- ✅ Use environment variables with `NEXT_PUBLIC_` prefix for client-side keys
- ✅ Use server-only environment variables (no prefix) for Admin keys
- ✅ Generate Secured API Keys on backend for multi-tenancy
- ✅ Route sensitive operations (indexing) through API routes only

**Operational Constraints**:
- Search-Only keys (lite client) are safe for frontend exposure
- Admin keys must remain in API routes (server-only)
- Use `algoliasearch/lite` in UI components, full `algoliasearch` only in API routes

## Examples

### Example 1: Basic Search Page

Minimal implementation with async page, client component, and Suspense boundary.

```typescript
// app/search/Search.tsx
'use client';
import { useMemo } from 'react';
import { liteClient as algoliasearch } from 'algoliasearch/lite';
import { InstantSearchNext, SearchBox, Hits } from 'react-instantsearch-nextjs';

const APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || '';
const API_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY || '';

export function Search() {
  const searchClient = useMemo(() => algoliasearch(APP_ID, API_KEY), []);
  
  return (
    <InstantSearchNext indexName="products" searchClient={searchClient}>
      <SearchBox />
      <Hits />
    </InstantSearchNext>
  );
}

// app/search/page.tsx
import { Suspense } from 'react';
import { Search } from './Search';

interface PageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export const dynamic = 'force-dynamic';

export default async function SearchPage({ searchParams }: PageProps) {
  await searchParams;
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Search />
    </Suspense>
  );
}
```

### Example 2: Search with Filters and URL Sync

Minimal implementation with RefinementList, URL synchronization, and TypeScript types.

```typescript
// app/search/Search.tsx
'use client';
import { useMemo } from 'react';
import { liteClient as algoliasearch } from 'algoliasearch/lite';
import { InstantSearchNext, SearchBox, Hits, RefinementList } from 'react-instantsearch-nextjs';

type ProductHit = {
  objectID: string;
  name: string;
  price: number;
  brand: string;
};

const APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || '';
const API_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY || '';

export function Search() {
  const searchClient = useMemo(() => algoliasearch(APP_ID, API_KEY), []);
  
  return (
    <InstantSearchNext
      indexName="products"
      searchClient={searchClient}
      routing={true}
    >
      <SearchBox />
      <RefinementList attribute="brand" />
      <Hits<ProductHit> hitComponent={({ hit }) => (
        <div>
          <h3>{hit.name}</h3>
          <p>${hit.price} - {hit.brand}</p>
        </div>
      )} />
    </InstantSearchNext>
  );
}
```

## Dependencies

This skill requires:
- `algoliasearch>=5.45.0`: Core Algolia client (use `/lite` for UI components)
- `react-instantsearch>=7.20.0`: React InstantSearch UI components
- `react-instantsearch-nextjs>=1.0.3`: Next.js App Router adapter
- `next>=15.0.0`: Next.js with App Router
- `react>=19.0.0`: React 19 (or RC during transition)

**Note**: For API-based deployments, all dependencies must be pre-installed. The skill cannot install packages at runtime.

## Performance Considerations

**Bundle Size**: Use `algoliasearch/lite` in UI components to reduce bundle size (excludes indexing logic).

**Client Initialization**: Singleton pattern prevents unnecessary re-initialization and network overhead.

**Suspense Boundaries**: Proper Suspense usage enables streaming and improves Time to First Byte (TTFB).

**URL Synchronization**: Built-in debouncing prevents excessive history stack operations.

## Related Resources

For extensive reference materials:
- Algolia v5 Documentation: https://www.algolia.com/doc/api-client/getting-started/install/javascript/
- Next.js 15 App Router: https://nextjs.org/docs/app
- React 19 Release Notes: https://react.dev/blog/2024/04/25/react-19

## Notes

- The version triad (Algolia v5, react-instantsearch 7.20.0, react-instantsearch-nextjs 1.0.3) is on the "bleeding edge" - monitor for updates
- `react-instantsearch-nextjs` is experimental - prepare for potential breaking changes in 1.x lifecycle
- React 19 compiler may reduce need for manual `useMemo` in future, but explicit memoization remains safest for now
- Always use `export const dynamic = 'force-dynamic'` for search pages to prevent static generation failures

