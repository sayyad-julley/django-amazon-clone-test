---
name: declarative-interaction-manager
description: Manages user interactions using React 19 Actions API, useActionState, and useTransition for non-blocking clinical workflows. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - react>=19.0.0
  - next>=15.0.0
---

# Declarative Interaction Management (Platform 1.0)

## Overview
Transitions from manual `useState` loading flags to React 19's native action lifecycle. This ensures a responsive UI thread for clinicians, even during computationally expensive or high-latency operations such as updating care plans or generating insurance claims.

## When to Use
- Implementing clinical note submissions via Server Actions.
- Managing long-running background updates (e.g., generating medical insurance claims).
- Preventing duplicate medical orders by disabling interactions during pending states.
- Providing instant predictive feedback for common clinician tasks (e.g., toggling medication status).

## React 19 Action Orchestration

### 1. Enhanced Form Handling (`useActionState`)
Formerly `useFormState`. Use this to manage form submissions, handle server-side validation (e.g., dose warnings), and track state changes without manual event handlers.

```tsx
"use client";
import { useActionState } from 'react';

export function PrescriptionForm({ submitAction }: { submitAction: any }) {
  const [state, formAction, isPending] = useActionState(submitAction, null);

  return (
    <form action={formAction}>
      <input name="medication_name" />
      {state?.errors?.dose && <span className="warning">{state.errors.dose}</span>}
      <button disabled={isPending}>Submit Order</button>
    </form>
  );
}
```

### 2. Deeply Nested Status (`useFormStatus`)
Allows sub-components (like a SaveButton) to detect if their parent form is pending a response, automatically enabling "busy" indicators without prop drilling.

```tsx
import { useFormStatus } from 'react-dom';

const ClinicalSaveButton = () => {
  const { pending } = useFormStatus();
  return <Button loading={pending} disabled={pending}>Confirm Order</Button>;
};
```

### 3. Non-blocking Background Updates (`useTransition`)
Mark clinical data updates (e.g., filtering a massive patient list) as non-urgent. This keeps the UI interactive for the clinician while the state update processes in the background.

```tsx
const [isPending, startTransition] = useTransition();

const handleDeepFilter = (query: string) => {
  startTransition(() => {
    // Heavy computation or background state update
    setPatientSearchQuery(query);
  });
};
```

### 4. Predictive UI (`useOptimistic`)
Provides instant visual feedback for common tasks while the server processes the actual mutation.

```tsx
// Instant check-off for medication administration
const [optimisticMed, addOptimisticMed] = useOptimistic(
  medication,
  (state, newStatus) => ({ ...state, status: newStatus })
);
```

## Anti-Patterns
- ❌ **Imperative Handlers**: Don't use `onClick={async (e) => ...}` for form submissions. Use declarative `<form action={...}>`.
- ❌ **Global Loading Spinners**: Avoid blocking the entire clinician dashboard. Use granular `isPending` states for local components.
- ❌ **Race Conditions**: Relying on manual flags to prevent double-submissions instead of React 19's native action management.

## Benefit for Clinicians
- **Responsiveness**: The UI thread remains open even during heavy background tasks.
- **Safety**: Built-in prevention of double-ordering via automated pending states.
- **Predictability**: Instant feedback via optimistic updates reduces perceived latency.
