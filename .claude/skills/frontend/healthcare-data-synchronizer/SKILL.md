---
name: healthcare-data-synchronizer
description: Handles complex clinical data synchronization using FHIR R4 standards, Ably WebSockets, and Next.js 15 caching strategies. Aligned with Platform 1.0 "Bleeding Edge Stability" strategy.
version: 1.1.0
dependencies:
  - next>=15.0.0
  - ably>=1.2.0
  - fhir-react>=1.0.0
  - typescript>=5.0.0
---

# Healthcare Data Synchronization (Platform 1.0)

## Overview
High-compliance healthcare systems require "Real-time Freshness" and strict adherence to interoperability standards like FHIR R4 and ABDM. This skill focuses on the "Poke/Pull" architectural pattern, ensuring that clinical data remains accurate without overloading client-side resources.

## When to Use
- Handling FHIR R4 resources (Patient, Observation, MedicationOrder).
- Implementing real-time vital sign updates or emergency clinical alerts.
- Optimizing data fetching in Next.js 15 where caching defaults have been reversed.

## Platform 1.0 Synchronization Patterns

### 1. Caching Reversals (Next.js 15)
Next.js 15 adopts a `no-store` default strategy for fetch requests. Clinicians must never be presented with stale diagnostic results.
- **Rule**: Explicitly opt-in for caching ONLY for static medical terminology or hospital protocols using `{ cache: 'force-cache' }`.
- **Default**: Assume all clinical data (vitals, encounter notes) is dynamic and must be fetched fresh.

### 2. "Poke/Pull" Synchronization
Instead of pushing massive clinical payloads over WebSockets, use a lightweight signaling mechanism.
- **Poke**: Server sends a minimal notification via Ably (e.g., `{ "type": "LAB_RESULT_READY", "patientId": "123" }`).
- **Pull**: Client receives the poke and triggers a React Query invalidation to "pull" the secured payload via the REST API.

### 3. FHIR R4 Integration
- **Type Safety**: Use TypeScript 5 and generated FHIR schemas to ensure every clinical property accessed is valid.
- **Visualization**: Leverage `fhir-react` components to render medical semantics (e.g., grouping active Conditions vs. historic Immunizations) within Ant Design layouts.

### 4. WebSocket Presence & Locking
In multi-practitioner environments (e.g., a shared ward), use Ably's Presence SDK to prevent "Edit Collisions".
- Display live avatar stacks of clinicians viewing a record.
- Implement component-level locking when a high-priority update is in progress.

## Anti-Patterns
- ❌ **Stale Clinical Cache**: Relying on framework-level implicit caching for diagnostic data (Next.js 14 behavior).
- ❌ **Payload Injection**: Sending raw PII/PHI directly through a WebSocket message. Always use the "Poke/Pull" pattern to keep data within secured REST channels.
- ❌ **Non-Standard Mapping**: Manual JSON parsing of medical records without FHIR R4 schema validation.

## Real-World Example: Critical Lab Alert
An abnormal lab value is detected in the backend. An Ably "poke" is sent to the clinician's dashboard. The `healthcare-data-synchronizer` handles the signal, invalidates the `lab-results` query, and pulls the fresh FHIR `DiagnosticReport`, which is then rendered with a high-priority "Urgent" status using the `css-layer-stylist` patterns.
