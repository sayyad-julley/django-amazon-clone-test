---
name: managing-hims-sdui
description: Controls dynamic clinical surfaces by delivering UI schemas directly from the backend to ensure real-time clinical agility. Use when a surface requires frequent updates without app store deployments (e.g., Nursing Checklists, Clinical Pathways, or Regulatory Forms).
version: 1.1.0
---

# Managing HIMS SDUI

## Overview
Server-Driven UI (SDUI) represents an extreme form of backend mapping where the server dictates not just the data, but the structure of the interface itself. In a HIMS environment, this agility is essential for deploying rapid changes to clinical protocols or nursing checklists without the delay of app store review processes. The client acts as a rendering engine, parsing JSON schemas and mapping them to a native Component Registry.

## When to Use
- **Clinical Pathways & Checklists**: When hospital protocols or nursing checklists change based on new regulations or specialized department needs (e.g., a new COVID triage flow).
- **Regulatory Forms**: For insurance or banking forms where the backend defines the schema, validation rules, and field order to ensure 100% compliance.
- **Dynamic Dashboarding**: Repurposing landing pages for public health alerts or seasonal campaigns via a CMS without engineering intervention.
- **Universal Agility**: Ensuring 100% adoption of UI changes on day one across iOS, Android, and Web.

## Technical Context
- **Infrastructure**: Redis 7 for high-performance caching of layout definitions.
- **Client Library**: React 19 (Web) and Native Component Registries.
- **Design System**: Ant Design 5.x and Tailwind CSS integration.
- **Performance**: Strategic caching and content checksums to minimize "Time to Interactive."

## Execution Steps

### Step 1: Manage Layout Definitions in Redis 7
Fetch the view structure schema, including component types, styles, and layout arrangements.

```json
// Example SDUI Payload for a Nursing Checklist
{
  "layoutId": "NURSING_FLOW_V2",
  "checksum": "a1b2c3d4",
  "components": [
    {
      "type": "VITAL_INPUT",
      "id": "bp_reading",
      "props": { "label": "Blood Pressure", "required": true, "validation": "^\\d{2,3}/\\d{2,3}$" }
    },
    {
      "type": "MEDICATION_PICKER",
      "id": "drug_admin",
      "props": { "stockCheck": true }
    }
  ]
}
```

### Step 2: Render via Component Registry
Parse the schema and map identifiers to native components.

```typescript
// Client-side Component Registry
const HIMS_COMPONENTS = {
  VITAL_INPUT: (props) => <VitalInputField {...props} />,
  MEDICATION_PICKER: (props) => <MedicationSelector {...props} />,
  // Graceful Fallback for unknown types
  UNKNOWN: (id) => <FallbackAlert componentId={id} />
};

function SDRenderer({ schema }) {
  return schema.components.map(comp => {
    const Component = HIMS_COMPONENTS[comp.type] || HIMS_COMPONENTS.UNKNOWN;
    return <Component key={comp.id} {...comp.props} />;
  });
}
```

## Transformation Rules
1. **Schema Versioning**: Strict versioning must be used. If the schema expects a component not found in the client's `HIMS_COMPONENTS` registry, the renderer MUST use the `UNKNOWN` fallback to prevent crashes.
2. **Contextual Logic**: Validation rules and action handlers (e.g., `onSave`) should be defined in the schema to ensure the UI remains a pure presentation layer.

## Workflow Checklist
- [x] Fetched JSON layout definition from Redis 7.
- [x] Mapped dynamic `type` identifiers to the native Component Registry.
- [x] Implemented versioning fallbacks for unknown component types.
- [x] Verified that validation rules are server-dictated and client-enforced.

## Validation Loop
1. **Consistency Check**: Verify that the same layout definition is served to all platforms to ensure 100% UI consistency.
2. **Performance Audit**: Ensure that Redis 7 response times for layout definitions are < 50ms to maintain a fluid user experience.

## Error Handling
- **Malformed Schema**: If the JSON fails parsing, revert to the `LATEST_STABLE` layout version stored in the local client cache.
- **Fallbacks**: Always render a "Contact IT" or "Update App" placeholder for mission-critical components that fail to render.
