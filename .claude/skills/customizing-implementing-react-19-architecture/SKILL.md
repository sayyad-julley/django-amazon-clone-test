---
dependencies:
- react>=19.0.0
- typescript>=5.0.0
description: Implements React 19 architecture by applying proven patterns (Server
  Components as default with composition, Server Actions for mutations with validation,
  use API for Promise unwrapping, useOptimistic for immediate UI updates, useActionState
  for form lifecycle, cookie-based authentication, parallel data fetching, Transitions
  for non-urgent updates), following best practices (component interleaving, serialization
  constraints, mandatory validation/auth, useFormStatus for submit state), implementing
  workarounds (CSS-in-JS Style Registry, Redux per-request initialization, Server
  Action testing with mocks, E2E testing for Server Components), and avoiding anti-patterns
  (waterfall fetch, use server poisoning, useEffect for data fetching, direct SC import
  into CC, non-serializable props, bearer token in LocalStorage). Use when building
  React 19 applications, migrating from React 18, implementing Server Components,
  setting up authentication, or avoiding common React 19 pitfalls.
name: implementing-react-19-architecture
version: 1.0.0
---

# Implementing React 19 Architecture

## Overview

React 19 represents a fundamental architectural shift from client-centric synchronization to server-side composition. The framework internalizes concurrency and server-side rendering capabilities directly into the core, transitioning from the useEffect era to declarative data primitives. This skill provides patterns for Server Components (RSC), Actions, the unified use API, optimistic UI, and authentication architecture, emphasizing composition-first design and action-driven state management.

## When to Use

Use this skill when:
- Building React 19 applications with Server Components
- Migrating from React 18 to React 19
- Implementing Server Actions for mutations
- Setting up authentication with cookie-based sessions
- Implementing optimistic UI patterns
- Avoiding common React 19 pitfalls (waterfall fetches, "use server" poisoning, useEffect misuse)

**Input format**: React 19.0.0+ project, Next.js 15+ (for RSC support) or compatible framework, TypeScript configuration, understanding of Server/Client component boundaries

**Expected output**: Production-ready React 19 implementation following proven patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- React 19.0.0+ project setup
- Next.js 15+ (for RSC support) or compatible framework
- TypeScript configuration for type safety
- Understanding of Server/Client component boundaries
- Access to validation library (Zod) for Server Actions

## Quick Start

### Server Components
See [resources/PATTERNS.md](resources/PATTERNS.md#server-components-architecture) for detailed patterns.

```typescript
export default async function Component() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}
```

### Server Actions
See [resources/PATTERNS.md](resources/PATTERNS.md#server-actions-implementation) for detailed patterns.

```typescript
'use server';
export async function action(formData: FormData) {
  // Validation + execution
}
```

### use API
See [resources/PATTERNS.md](resources/PATTERNS.md#the-use-api) for detailed patterns.

```typescript
const data = use(promise);
```

## Navigation to Resources

**Patterns**: See [resources/PATTERNS.md](resources/PATTERNS.md) for:
- Server Components architecture
- Server Actions implementation
- use API patterns
- Optimistic UI with useOptimistic
- Form management with useActionState
- Transitions and concurrent features
- Data fetching patterns

**Anti-Patterns**: See [resources/ANTIPATTERNS.md](resources/ANTIPATTERNS.md) for:
- Waterfall fetch pattern
- "use server" poisoning
- useEffect misuse
- Direct SC import into CC
- Non-serializable props
- Bearer token in LocalStorage

**Workarounds**: See [resources/WORKAROUNDS.md](resources/WORKAROUNDS.md) for:
- CSS-in-JS Style Registry
- Redux integration strategies
- Testing Server Actions
- Testing Server Components

**Authentication**: See [resources/AUTHENTICATION.md](resources/AUTHENTICATION.md) for:
- Cookie-based session management
- Server Action security
- Session verification patterns

**Testing**: See [resources/TESTING.md](resources/TESTING.md) for:
- Unit testing Server Actions
- Integration testing strategies
- E2E testing patterns

## Common Patterns

### Composition Pattern (SC as children to CC)
Pass Server Components as children prop to Client Components to maintain zero bundle size for the parent.

### Optimistic Mutation Pattern
Use useOptimistic to provide immediate UI feedback while server actions process, with automatic rollback on failure.

### Promise Unwrapping Pattern
Pass Promise objects to components and unwrap with use() to decouple fetching initiation from data consumption.

### Form Action Pattern
Use useActionState for form lifecycle management and useFormStatus for submit state without prop drilling.

## Code Templates

### Template 1: Server Component with Data Fetching
```typescript
export default async function Component() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}
```

### Template 2: Server Action with Validation
```typescript
'use server';
export async function action(formData: FormData) {
  // Validation + execution
}
```

### Template 3: useActionState Form
```typescript
const [state, formAction] = useActionState(action, null);
```

### Template 4: useOptimistic Mutation
```typescript
const [optimistic, addOptimistic] = useOptimistic(state, reducer);
```

### Template 5: use(Promise) Pattern
```typescript
const data = use(promise);
```

## Real-World Examples

### Example 1: Production-Ready Auth Form

```typescript
// app/actions.ts
'use server';
import { z } from 'zod';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export type ActionState = {
  errors?: { email?: string; password?: string; _form?: string };
  fields?: { email?: string };
};

export async function login(prevState: ActionState | null, formData: FormData): Promise<ActionState> {
  const data = Object.fromEntries(formData);
  const parsed = schema.safeParse(data);
  
  if (!parsed.success) {
    return {
      errors: parsed.error.flatten().fieldErrors,
      fields: { email: data.email as string },
    };
  }
  
  const isValid = await checkCredentials(parsed.data);
  if (!isValid) {
    return { errors: { _form: ['Invalid credentials'] }, fields: { email: data.email as string } };
  }
  
  cookies().set('session', 'secure-token', { httpOnly: true, secure: true });
  redirect('/dashboard');
}

// app/components/LoginForm.tsx
'use client';
import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';
import { login } from '../actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending} type="submit" className="btn-primary">
      {pending ? 'Signing In...' : 'Sign In'}
    </button>
  );
}

export default function LoginForm() {
  const [state, formAction] = useActionState(login, null);
  return (
    <form action={formAction} className="space-y-4">
      {state?.errors?._form && <div className="error">{state.errors._form}</div>}
      <div>
        <label htmlFor="email">Email</label>
        <input name="email" defaultValue={state?.fields?.email} />
        {state?.errors?.email && <p>{state.errors.email}</p>}
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input name="password" type="password" />
        {state?.errors?.password && <p>{state.errors.password}</p>}
      </div>
      <SubmitButton />
    </form>
  );
}
```

### Example 2: Optimistic Comment Thread

```typescript
'use client';
import { useOptimistic, useRef } from 'react';
import { postComment } from './actions';

export function CommentThread({ comments }: { comments: Comment[] }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [optimisticComments, addOptimistic] = useOptimistic(
    comments,
    (state, newComment: string) => [...state, { id: 'temp', text: newComment, pending: true }]
  );

  async function action(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimistic(text);
    formRef.current?.reset();
    await postComment(formData);
  }

  return (
    <div>
      {optimisticComments.map((c) => (
        <div key={c.id} style={{ opacity: c.pending ? 0.5 : 1 }}>
          {c.text} {c.pending && '(Sending...)'}
        </div>
      ))}
      <form action={action} ref={formRef}>
        <input name="text" required />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## Error Handling

### Server Action Error Handling
Return error objects from Server Actions and display them in the UI using useActionState:

```typescript
export async function action(formData: FormData) {
  try {
    // Operation
    return { success: true };
  } catch (error) {
    return { errors: { _form: ['Operation failed'] } };
  }
}
```

### Validation Error Display
Use Zod's safeParse to return structured validation errors:

```typescript
const parsed = schema.safeParse(data);
if (!parsed.success) {
  return { errors: parsed.error.flatten().fieldErrors };
}
```

### Network Error Handling
For use(Promise) patterns, handle errors with Error Boundaries or try-catch in async Server Components.

## Security Guidelines

**CRITICAL**: Never hardcode sensitive information:
- ❌ No API keys, passwords, or tokens in code
- ❌ No credentials in SKILL.md or scripts
- ✅ Use external credential management systems
- ✅ Route sensitive operations through secure channels

**Input Validation**: All Server Action inputs must be validated using libraries like Zod before processing any FormData.

**Authentication Checks**: Server Actions must verify the user's session. It is unsafe to rely solely on the component rendering the button to check permissions.

**Cookie Security**: Always use HttpOnly and secure flags when setting cookies in Server Actions.
