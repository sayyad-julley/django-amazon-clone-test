---
name: orchestrating-hims-bff
description: Optimizes experience-layer data aggregation and enforces DPDP-compliant PII filtering. Leverages Next.js 15 API routes to proxy Java 21 Spring Boot services using Virtual Threads (Project Loom) for massive concurrency. Use when a UI view requires data from multiple microservices or when masking internal IDs for security and data sovereignty.
version: 1.1.0
---

# Orchestrating HIMS BFF

## Overview
The Backend-For-Frontend (BFF) pattern in HIMS Platform 1.0 is an experience-centric architectural response to divergent frontend requirements (Web, Mobile, IoT). It acts as a dedicated translation and orchestration layer, sitting at the network perimeter and functioning as a specialized API Gateway. By moving beyond a "One-Size-Fits-All" API strategy, the BFF ensures that clinical dashboards remain performant and compliant with the Indian Digital Personal Data Protection (DPDP) Act.

## When to Use
- **Microservice Aggregation**: When a clinical dashboard must display data from multiple sources (Identity, EMR, Billing) in a single response, solving the "Chatty I/O" and "N+1 Problem."
- **Data Sovereignty**: When ensuring zero patient data exfiltration from the VPC by filtering Personal Identifiable Information (PII) before it reaches the logging layer of the ELK Stack.
- **Protocol Translation**: Mapping internal gRPC communication to REST/JSON for web and mobile consumers.
- **Performance Optimization**: Minimizing payload sizes and HTTP requests on variable hospital 3G/4G networks.

## Technical Context
- **Frontend**: Next.js 15 API Routes (acting as the BFF vehicle).
- **Core Backend**: Java 21 with Virtual Threads (Project Loom) for non-blocking aggregation.
- **Identity & Auth**: Scalekit for session management and Scale-out auth.
- **Authorization**: Permit.io for ReBAC (Relationship-Based Access Control) and ABAC (Attribute-Based Access Control) enforcement.
- **Infrastructure**: Kong Gateway for traffic routing and consolidated ELK Stack for observability.

## Execution Steps

### Step 1: Orchestrate High-Concurrency aggregation
Utilize the massive throughput capabilities of Project Loom's Virtual Threads to perform non-blocking I/O across multiple microservices.

```typescript
// Next.js 15 API Route acting as BFF Aggregator
import { fetchEMR, fetchBilling, fetchPatient } from '@/lib/api-client';
import { enforcePolicy } from '@/lib/permit-service';

export async function GET(request: Request) {
  // Authorization Check via Permit.io (ABAC/ReBAC)
  const isAuthorized = await enforcePolicy(request, 'view_dashboard');
  if (!isAuthorized) return Response.json({ error: 'AUTH_001' }, { status: 403 });

  // Aggregate clinical data concurrently
  // The Java 21 backend handles these requests via Virtual Threads
  const [patient, emr, billing] = await Promise.all([
    fetchPatient(requestId),
    fetchEMR(patientId),
    fetchBilling(patientId)
  ]);

  return Response.json(shapeDashboardPayload(patient, emr, billing));
}
```

### Step 2: Mask Sensitive Identities
Apply the "Anti-Corruption Layer" logic to ensure internal database IDs or PII never leak to the client side.

```typescript
function shapeDashboardPayload(patient, emr, billing) {
  return {
    patientId: maskId(patient.id), // Replace internal ID with external reference
    vitals: emr.vitals,
    balance: billing.total_due,
    // Sensitive PII (Phone/National ID) is filtered here
  };
}
```

## Transformation Rules
1. **PII Filtering**: Any field marked as PII in the VPC security manifest MUST be removed or tokenized before being included in the BFF response.
2. **Standardized Errors**: Map internal Java exceptions to stable, machine-readable error codes (e.g., `EMR_SERVICE_DOWN`) for frontend translation.
3. **Session Cookies**: Leverage Scalekit's secure cookie mechanism to maintain state without exposing internal session IDs.

## Workflow Checklist
- [x] Intercepted multi-service requests at the network perimeter (Kong Gateway).
- [x] Performed high-concurrency non-blocking I/O via Virtual Threads.
- [x] Enforced fine-grained ReBAC/ABAC policies via Permit.io.
- [x] Masked internal IDs and filtered PII to maintain DPDP compliance.

## Validation Loop
1. **Security Audit**: Trigger the "Security Audit Skill" to verify that no PII is visible in the ELK logging layer of this BFF route.
2. **Latency Test**: Verify that the "Time to Interactive" (TTI) for aggregated results remains within the "Performance First" threshold (e.g., < 200ms overhead).

## Error Handling
- **Partial Failure**: If `fetchBilling` fails, return the clinical data with a `billingStatus: 'UNAVAILABLE'` flag to prevent whole-page failures.
- **Auth Rejection**: Return `AUTH_001` (Unauthorized) or `AUTH_002` (Forbidden) for the frontend to handle localized messaging.
