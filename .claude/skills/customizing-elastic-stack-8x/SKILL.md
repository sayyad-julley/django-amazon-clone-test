---
name: implementing-elastic-stack-8x-hims
description: Implements and optimizes the Elastic Stack (ELK v8.x) for HIMS Platform 1.0. Applies patterns for Kafka buffering, Hot-Warm-Cold storage, and Java 21 threading. Handles PII redaction for DPDP compliance and Debezium CDC syncing. Use when setting up observability, search, or audit trails for clinical systems.
version: 1.0.0
dependencies:
  - elasticsearch>=8.15.0
  - logstash>=8.15.0
  - kibana>=8.15.0
  - opentelemetry>=2.23.0
  - debezium>=2.5
---

# Implementing Elastic Stack 8.x for HIMS

## Overview

This skill provides architectural patterns and implementation standards for deploying the Elastic Stack (ELK) within the HIMS Platform 1.0. It focuses on high-concurrency Java 21 environments, clinical data integrity, and compliance with India's DPDP Act.

## Execution Steps

### Step 1: Initialize Ingestion Pipeline
1.  **Configure Logstash**: Use persistent queues (PQ) for resiliency.
2.  **Setup Kafka Buffering**: Decouple ingestion from indexing to handle traffic surges.
3.  **HIMS Specifics**: Ensure Logstash is configured to handle Debezium CDC events.

### Step 2: Implement Data Tiers (ILM)
1.  **Hot Tier**: SSD-backed nodes for real-time indexing.
2.  **Warm Tier**: Force-merge segments for search performance.
3.  **Cold/Frozen**: Use searchable snapshots for archival clinical data.

### Step 3: Hardening & Compliance
1.  **PII Redaction**: Apply Logstash filter rules to mask patient data.
2.  **Explicit Mapping**: Avoid dynamic mapping for clinical fields (e.g., FHIR IDs).

---

## Detailed Resources

- **Technical Reference**: See [resources/REFERENCE.md](resources/REFERENCE.md) for Java 21 threading, DPDP compliance, and case studies.
- **Code Templates**: See [templates/TEMPLATES.md](templates/TEMPLATES.md) for Logstash pipelines, ES mappings, and Docker configs.

---

## Common Patterns

### 1. Kafka Buffering Pattern
Protects Elasticsearch from ingestion spikes. Filebeat -> Kafka -> Logstash -> Elasticsearch.

### 2. Hot-Warm-Cold Architecture
Optimizes storage cost vs. search speed. Rollover at 50GB or 7 days.

### 3. Outbox Pattern for CDC
Ensures "exactly-once" delivery of clinical updates from PostgreSQL to Elasticsearch via Debezium.

---

## Workarounds

| Challenge | Workaround |
| :--- | :--- |
| **Java 21 Pinning** | Use Asynchronous Appenders or OTLP/gRPC to avoid `synchronized` blocks. |
| **PII Data Leak** | Use Logstash `redact` filter or Elastic NER models before indexing. |
| **Relational Data** | Denormalize at source or use the **Enrich Processor** during ingestion. |

---

## Anti-Patterns to Avoid

- **Over-Sharding**: Too many small shards (>20 per GB of heap) leads to cluster instability.
- **Mapping Explosion**: Logging arbitrary JSON without schema control crashing master nodes.
- **Dynamic Mapping for IDs**: Clinical IDs guessed as integers instead of keywords (causing conflicts).
- **In-Memory Queues**: Reliance on default Logstash queues leading to data loss during crashes.
