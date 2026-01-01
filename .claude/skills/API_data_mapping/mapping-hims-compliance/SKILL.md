---
name: mapping-hims-compliance
description: Ensures clinical data adherence to Indian national standards (ABDM) and standardizes data for interoperability using FHIR R4. Use when clinical data must be serialized for national health repositories or when forensic-grade audit trails are required.
version: 1.1.0
---

# Mapping HIMS Compliance

## Overview
Compliance in HIMS Platform 1.0 is built on the strategy of "Bleeding Edge Stability." This skill directs agents to map relational clinical data to international interoperability standards (FHIR R4) and the Ayushman Bharat Digital Mission (ABDM) guidelines. It ensures that the system remains compliant with the Digital Personal Data Protection (DPDP) Act by enforcing zero patient data exfiltration from the hospital's Virtual Private Cloud (VPC).

## When to Use
- **National Interoperability**: When serializing health records into FHIR R4 bundles for submission to the National Health Authority (NHA) gateway.
- **Forensic Auditing**: When utilizing Debezium to capture database-level changes and mapping them to immutable Kafka topics for clinical auditing.
- **Sovereignty Enforcement**: When verifying that no Personal Identifiable Information (PII) is transmitted to third-party processors outside the VPC.
- **Standardized Error Mapping**: When mapping machine-readable clinical error codes (e.g., `AUTH_001`) to localized, user-friendly strings on the frontend.

## Technical Context
- **Standards**: Ayushman Bharat Digital Mission (ABDM), FHIR R4.
- **Libraries**: HAPI FHIR 7.0.0 for Java-based serialization.
- **Data Engineering**: Debezium (CDC) and Kafka 7.5 for clinical event streams.
- **Database**: PostgreSQL 16 (Relational Source for clinical entities).

## Execution Steps

### Step 1: Serialize to FHIR R4 Bundles
Instruction: Utilize the HAPI FHIR library to parse relational data into compliant resources. Ensure that timestamps are stored in UTC format.

```java
// Spring Boot FHIR Serialization Logic
Patient fhirPatient = new Patient()
    .addIdentifier(new Identifier().setSystem("https://ndhm.gov.in").setValue(abhaId))
    .addName(new HumanName().addGiven(firstName).setFamily(lastName));

// Encode as JSON for transmission
String jsonBundle = fhirContext.newJsonParser().encodeResourceToString(fhirPatient);
```

### Step 2: Map Database Changes (CDC) to Kafka
Instruction: Analyze database schema updates captured by Debezium and ensure the resulting Kafka events are mapped correctly to clinical resource types.

```python
# Script: map_cdc_to_fhir.py
def process_message(kafka_msg):
    # Map raw Debezium 'after' state to FHIR Bundle
    if kafka_msg['op'] == 'u': # Update operation
        return map_to_fhir_v2(kafka_msg['after'])
```

## Transformation Rules
1. **Timezone Policy**: All raw database values MUST be stored in UTC format. Conversion occurs only at the presentation layer.
2. **PII Masking**: Sensitive identifiers (e.g., Phone, Aadhar) MUST be filtered before reaching any logging or non-clinical processing layer.
3. **Machine-Readable Errors**: Errors MUST return stable codes (e.g., `AUTH_001`, `VALIDATION_005`) to allow the frontend to handle translations.

## Workflow Checklist
- [x] Utilized HAPI FHIR library for ABDM-compliant serialization.
- [x] Mapped PostgreSQL updates (via Debezium) to immutable Kafka topics.
- [x] Validated that zero PII is transmitted outside the secure VPC.
- [x] Ensured all clinical timestamps are normalized to UTC.

## Validation Loop
1. **FHIR Validation**: Run the HAPI FHIR Validator against the generated bundle to ensure compliance with ABDM profiles.
2. **Sovereignty Check**: Verify via the Kong Gateway logs that no unencrypted PII has crossed the network perimeter.

## Error Handling
- **Mapping Failure**: If a database record cannot be mapped to a valid FHIR resource, quarantine the event in a "Compliance DLQ" for manual review.
- **Unauthorized Egress**: If PII filtering fails, immediately terminate the connection and log a security incident.
