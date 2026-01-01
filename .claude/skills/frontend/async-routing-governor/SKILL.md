---
name: async-routing-governor
description: Enforces Next.js 15 Asynchronous Request API patterns and fine-grained clinical policy enforcement via Permit.io. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - next>=15.0.0
  - permitio-sdk-python>=2.0.0
  - react>=19.0.0
---

# Async Routing & Governance (Platform 1.0)

## Overview
Next.js 15 introduces a fundamental shift to "Async All The Way" for dynamic request data. This skill ensures clinical applications properly handle asynchronous `params`, `cookies`, and `headers` while integrating robust, policy-driven component visibility for sensitive medical records.

## When to Use
- Accessing Patient IDs or Hospital Tenant contexts from Next.js 15 URL parameters.
- Verifying fine-grained clinical policies (e.g., "Can this nurse view psychiatric notes?") using Permit.io.
- Implementing role-based component visibility in high-density clinical dashboards.

## Governance Patterns

### 1. Asynchronous Request APIs (Next.js 15)
In Platform 1.0, dynamic APIs are treated as Promises. You MUST `await` them to optimize rendering paths and support progressive streaming.

| API | Next.js 15 Requirement | Clinical Impact |
| :--- | :--- | :--- |
| `params` | Awaitable Promise | Necessary for deep-linking into specific patient encounters. |
| `searchParams` | Awaitable Promise | Maintains complex filters in diagnostic dashboards. |
| `cookies()` | Must be Awaited | Enhances B2B tenant onboarding security. |
| `headers()` | Must be Awaited | Critical for verifying policy tokens from Permit.io. |

```tsx
// Example: Awaiting params in a clinical route
export default async function PatientPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const patient = await fetchPatientResource(id);
  // ...
}
```

### 2. Fine-Grained Policy Enforcement (Permit.io)
Utilize a Hybrid Security Model where Permit.io provides ABAC/RBAC at the component level.
- **Rule**: Never rely solely on client-side role checks (e.g., `if (user.role === 'MD')`).
- **Pattern**: Verify policies in Server Components before rendering sensitive UI elements (e.g., "Delete Record" or "Modify Dosage").

### 3. Data Sovereignty & Audit Integrity
- **Sovereign Observability**: Ensure all front-end traces and metrics are routed to the internal OpenTelemetry pipeline within the VPC.
- **Audit Logs**: Ensure that destructive actions in the UI trigger events captured by the internal Kafka pipeline, providing a forensic-grade audit log.

## Anti-Patterns
- ❌ **Synchronous Parameter Access**: Attempting to destructure `{ id }` directly from props without `await` in Next.js 15.
- ❌ **VPC Exfiltration**: Using third-party SaaS observability tools that route PHI/PII outside the sovereign virtual private cloud.
- ❌ **Static Auth Over-reliance**: Using monolithic "Admin/User" roles for complex clinical permissions instead of fine-grained policies.

## Real-World Example: Medication Edit Constraint
A clinician navigates to a patient's medication list. The `async-routing-governor`:
1. `awaits` the `searchParams` to apply active filtering.
2. `awaits` a Permit.io policy check for the specific medication resource.
3. Renders the "Edit Dosage" button only if the policy allows, ensuring data governance at the point of care.
