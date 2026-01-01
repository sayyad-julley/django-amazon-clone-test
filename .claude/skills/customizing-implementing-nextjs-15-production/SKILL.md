---
dependencies:
- next>=15.0.0
- react>=19.0.0
- typescript>=5.0.0
description: Implements Next.js 15 production patterns by applying proven strategies
  (async request APIs with await params/cookies/headers, dynamic-by-default caching
  with explicit force-cache opt-in, use cache directive, React 19 compiler, Partial
  Prerendering, validated Server Actions with Zod, optimistic UI with useOptimistic,
  middleware optimization), following best practices (explicit caching, server-only
  boundaries, staleTimes config, React Compiler memoization), implementing workarounds
  (React 19 peer dependency conflicts, hydration errors, Turbopack issues), and avoiding
  anti-patterns (synchronous API access, database calls in middleware, client fetch
  waterfalls, secret leakage, implicit caching). Use when building Next.js 15 apps,
  migrating from Next.js 14, implementing async patterns, configuring caching, or
  avoiding common pitfalls.
name: implementing-nextjs-15-production
version: 1.0.0
---

# Implementing Next.js 15 Production

## Overview

Next.js 15 shifts to "dynamic-by-default" architecture. Key changes: Async request APIs, inverted caching defaults, React 19 compiler. Focus: Production patterns, anti-patterns, workarounds.

## When to Use

Use this skill when:
- Building Next.js 15 applications with App Router
- Migrating from Next.js 14 (async API migration)
- Implementing Partial Prerendering (PPR) patterns
- Configuring explicit caching strategies
- Setting up React 19 compiler
- Avoiding common pitfalls (synchronous API access, middleware anti-patterns)

**Input format**: Next.js 15+ project, understanding of async/await, TypeScript configuration

**Expected output**: Production-ready implementation following patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

- Next.js 15+ project with App Router
- React 19 RC+ installed
- TypeScript configuration
- Understanding of async/await patterns

## Core Patterns

### Pattern 1: Asynchronous Request APIs

```typescript
// Async page component
interface PageProps {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}
export default async function Page(props: PageProps) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  // Use params and searchParams
}

// Client component with use()
'use client';
import { use } from 'react';
export default function ClientPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  return <div>{id}</div>;
}

// Async cookies/headers
const cookieStore = await cookies();
const headersList = await headers();
```

### Pattern 2: Dynamic-by-Default Caching

```typescript
// Explicit force-cache for static data
const data = await fetch(url, { next: { revalidate: 3600 } });

// use cache directive
import { cacheTag } from 'next/cache';
export async function getData() {
  'use cache';
  cacheTag('data');
  return expensiveOperation();
}

// staleTimes configuration
// next.config.ts
experimental: { staleTimes: { dynamic: 30, static: 180 } }
```

### Pattern 3: Validated Server Actions

```typescript
// createSafeAction utility
export const createSafeAction = <TInput, TOutput>(
  schema: z.Schema<TInput>,
  handler: (data: TInput) => Promise<ActionState<TInput, TOutput>>
) => { /* implementation */ };

// Usage
const schema = z.object({ title: z.string().min(3) });
export const action = createSafeAction(schema, async (data) => {
  // Validated data
});
```

### Pattern 4: Optimistic UI

```typescript
const [optimistic, addOptimistic] = useOptimistic(state, reducer);
startTransition(() => addOptimistic(newValue));
await serverAction();
```

### Pattern 5: Composable Cache Pattern

```typescript
'use cache';
cacheTag('revenue-metrics');
const revenue = await db.order.aggregate({ /* ... */ });
```

## Best Practices

1. **Async Request Access**: Always await params/searchParams/cookies/headers. Use `use()` hook in Client Components for Promise unwrapping.

2. **Explicit Caching**: Opt-in to caching for static content with `force-cache`. Use `use cache` for expensive computations. Configure `staleTimes` appropriately.

3. **Server Action Validation**: Always validate Server Actions with Zod. Use `createSafeAction` pattern for type safety and security.

4. **Middleware Optimization**: Exclude static assets from middleware matcher. Keep middleware lightweight (no database calls, only routing/auth checks).

5. **React Compiler**: Enable React Compiler for automatic memoization. Remove manual `useMemo`/`useCallback` where compiler handles it.

## Workarounds

### React 19 Peer Dependency Conflicts

```json
// package.json
{
  "overrides": {
    "react": "$react",
    "react-dom": "$react-dom"
  }
}
// Or: npm install --legacy-peer-deps
```

### Hydration Errors with Third-Party Scripts

```typescript
<div suppressHydrationWarning>
  {new Date().toLocaleTimeString()}
</div>
// Use sparingly - only for known third-party script conflicts
```

### Turbopack Barrel File Issues

```bash
next dev --webpack  # Fallback to Webpack if Turbopack fails
```

## Anti-Patterns

### 1. Synchronous Dynamic API Access

```typescript
// ❌ Anti-Pattern
export default function Page({ params }) {
  return <h1>{params.id}</h1>; // Error: params is Promise
}

// ✅ Correct
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <h1>{id}</h1>;
}
```

### 2. Database Calls in Middleware

```typescript
// ❌ Anti-Pattern: Prisma in middleware
export default middleware(async (req) => {
  const user = await db.user.findUnique({ where: { id } }); // Edge Runtime doesn't support
});

// ✅ Correct: Middleware only for routing/auth checks
export default middleware((req) => {
  const token = req.cookies.get('token');
  if (!token) return NextResponse.redirect('/login');
});
```

### 3. Client-Side Fetch Waterfalls

```typescript
// ❌ Anti-Pattern: Chained useEffect fetches
'use client';
function Child({ parentId }) {
  useEffect(() => {
    fetch(`/api/child/${parentId}`).then(...); // Waits for parent
  }, [parentId]);
}

// ✅ Correct: Lift to Server Component
async function Parent() {
  const parent = await fetchParent();
  const children = await fetchChildren(parent.id); // Parallel on server
  return <Child data={children} />;
}
```

### 4. Leaking Secrets to Client

```typescript
// ❌ Anti-Pattern: Server utility in Client Component
'use client';
import { db } from '@/lib/db'; // Webpack might include in bundle

// ✅ Correct: Use server-only package
// lib/db.ts
import 'server-only';
export const db = /* ... */;
```

### 5. Implicit Caching Assumptions

```typescript
// ❌ Anti-Pattern: Assuming fetch is cached
const data = await fetch(url); // No cache in Next.js 15

// ✅ Correct: Explicit opt-in
const data = await fetch(url, { next: { revalidate: 3600 } });
```

## Examples

### Example 1: Blog Post Page with Async Params

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);
  return <article>{post.content}</article>;
}
```

### Example 2: Search Form with next/form

```typescript
// components/search.tsx
import Form from 'next/form';

export default function Search() {
  return (
    <Form action="/search" className="flex gap-2">
      <input name="query" placeholder="Search..." />
      <button type="submit">Search</button>
    </Form>
  );
}
```

## Error Handling

- **"params is a Promise"**: Always await params in Server Components
- **"Cannot use db in middleware"**: Move database calls to Server Components or Route Handlers
- **"Hydration mismatch"**: Use `suppressHydrationWarning` sparingly for third-party scripts
- **"Stale data"**: Explicitly opt-in to caching with `force-cache` or `use cache`
- **"Peer dependency conflict"**: Use `package.json` overrides or `--legacy-peer-deps`

## Security Guidelines

**CRITICAL**: Never hardcode sensitive information:

- ❌ No API keys, passwords, or tokens in code
- ❌ No credentials in SKILL.md or scripts
- ✅ Use external credential management systems
- ✅ Use `server-only` package to prevent client bundle inclusion
- ✅ Route sensitive operations through secure channels

