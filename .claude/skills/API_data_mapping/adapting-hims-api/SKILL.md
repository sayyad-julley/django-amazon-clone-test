---
name: adapting-hims-api
description: Implements an Anti-Corruption Layer on the frontend to normalize API data and decouple UI components from backend schema volatility. Use when the backend schema changes or when raw data formats (e.g., snake_case, UTC) must be converted for UI consumption.
version: 1.1.0
---

# Adapting HIMS API

## Overview
The Adapter Pattern acts as a structural "Anti-Corruption Layer" on the HIMS frontend. It ensures that UI components remain clean, focused on rendering, and decoupled from the internal database schemas reflected in backend APIs. By normalizing data immediately after retrieval, the frontend gains resilience against backend evolution (e.g., field renaming) and provides a superior user experience through immediate feedback (Optimistic UI).

## When to Use
- **Data Normalization**: Converting `snake_case` backend fields to `camelCase` frontend props.
- **Resilience against Volatility**: Renaming a backend field (e.g., `fname` to `first_name`) without touching hundreds of React components.
- **Optimistic UI & Offline-First**: Implementing logic to predict resulting states in state management (Zustand) before the server confirms an action.
- **Clinical Precision**: Converting UTC timestamps from the backend into the user’s local timezone only at the presentation layer.

## Technical Context
- **Framework**: Next.js 15 and React 19.
- **State Management**: Zustand (local state) and React Query (server state).
- **Type Safety**: Strict TypeScript 5.x types and Zod for runtime validation.
- **Aesthetics**: Decoupling allows UI components to focus on high-performance Ant Design / Tailwind transitions.

## Execution Steps

### Step 1: Implement the Anti-Corruption Normalizer
Intercept network responses and normalize data formats.

```typescript
// Example HIMS API Adapter Implementation
interface APIPatient {
  user_id: string;
  first_name: string;
  last_name: string;
  status: 'INPATIENT' | 'OUTPATIENT';
  vitals?: { heart_rate: number };
}

interface Patient {
  patientId: string;
  fullName: string;
  isAdmitted: boolean;
  heartRate: number;
}

const transformPatientData = (apiResponse: APIPatient): Patient => {
  return {
    patientId: apiResponse.user_id,
    fullName: `${apiResponse.first_name} ${apiResponse.last_name}`,
    isAdmitted: apiResponse.status === 'INPATIENT',
    // Safe default for clinical vitals to prevent UI breakage
    heartRate: apiResponse.vitals?.heart_rate ?? 0
  };
};
```

### Step 2: Implement Optimistic UI Logic
Predict state changes in Zustand to ensure immediate feedback in hospital environments.

```typescript
// Zustand Slice with Optimistic Update
const usePatientStore = create((set) => ({
  records: [],
  updateVital: async (id, heartRate) => {
    // 1. Optimistic Update
    set((state) => ({
      records: state.records.map(r => r.id === id ? { ...r, heartRate } : r)
    }));

    try {
      await api.post(`/vitals/${id}`, { heartRate });
    } catch (error) {
      // 2. Rollback on Failure
      set((state) => ({ /* restore previous state */ }));
    }
  }
}));
```

## Transformation Rules
1. **Case Normalization**: All incoming keys MUST be transformed to `camelCase`.
2. **Timezone Policy**: UTC strings from the backend MUST be converted to `Locale` only within the adapter function.
3. **Null Safety**: Provide default values (e.g., `Heart Rate: N/A`) within the adapter to prevent `undefined` properties from reaching components.

## Workflow Checklist
- [x] Intercepted network responses immediately after fetching via React Query.
- [x] Normalized field names and data types (Anti-Corruption Layer).
- [x] Converted UTC timestamps to user local time for presentation.
- [x] Implemented safe defaults for optional clinical fields.

## Validation Loop
1. **Schema Integrity**: Use a TypeScript utility to verify that all transformed objects strictly match the `frontend-models` declaration.
2. **Rollback Verification**: Simulate a network failure to ensure the Optimistic UI correctly rolls back the state without user intervention.

## Error Handling
- **Renamed Field**: If the adapter detects a missing expected field, log a `UI_SCHEMA_MISMATCH` alert to the ELK Stack while providing a safe fallback value.
- **Invalid Vitall Format**: If heart rate is returned as a string, attempt conversion to Number or default to 0.
