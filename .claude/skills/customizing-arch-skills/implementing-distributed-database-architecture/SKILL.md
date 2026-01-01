---
name: implementing-distributed-database-architecture
description: Implements scalable multi-tenant distributed database systems by applying patterns (Shared-Schema Multi-Tenancy, Transactional Outbox, CDC with Debezium, Tiered Storage, RLS, Expand-and-Contract), following best practices (co-location, RLS enforcement, log-based CDC, idempotency, partition pruning), implementing workarounds (Claim Check Pattern, Async Retrieval, Partitioned Retention), and avoiding anti-patterns (Dual Write, Cross-Shard Joins, Fat Payload, Application-Only Filtering, Polling, Missing Idempotency, Unrestricted Queries). Use when implementing multi-tenant SaaS, event-driven architectures, agentic systems requiring real-time context, or high-volume data systems requiring horizontal scaling.
version: 1.0.0
---

# Implementing Distributed Database Architecture

## Overview

Implements scalable multi-tenant distributed database systems using sharding, event-driven CDC, and tiered storage patterns. Provides patterns for Shared-Schema Multi-Tenancy (tenant_id distribution with co-location), Transactional Outbox (atomic event publishing), CDC with Debezium, Tiered Storage (Hot-Warm-Cold partitioning), RLS (tenant isolation), and Expand-and-Contract (zero-downtime schema evolution). Focuses on horizontal scalability, ACID guarantees in distributed environments, and agentic system integration.

## When to Use

Use this skill when:
- Implementing multi-tenant SaaS applications requiring tenant isolation and horizontal scaling
- Building event-driven microservices architectures with transactional consistency requirements
- Designing agentic systems requiring real-time database context for autonomous workflows
- Scaling high-volume data systems beyond single-node capacity
- Requiring ACID guarantees in distributed database environments
- Implementing zero-downtime schema migrations in production systems

**Input format**: Database cluster configuration, tenant count, throughput requirements, consistency requirements

**Expected output**: Production-ready distributed database architecture with patterns applied, best practices followed, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- PostgreSQL/Citus or MySQL/Vitess knowledge and cluster access
- Understanding of sharding concepts and distribution strategies
- Kafka cluster access and Debezium connector familiarity
- Database administration experience with replication and partitioning
- Network architecture knowledge for multi-node deployments

## Quick Start

### Key Patterns Summary

1. **Shared-Schema Multi-Tenancy**: tenant_id distribution column with co-location
2. **Row Level Security (RLS)**: Database-level tenant isolation policies
3. **Transactional Outbox**: Atomic event publishing via database transaction
4. **Change Data Capture (CDC)**: Debezium log-based streaming to Kafka
5. **Idempotency**: processed_events table for at-least-once delivery handling
6. **Tiered Storage**: Hot-Warm-Cold partitioning with pg_partman
7. **Expand-and-Contract**: 5-phase zero-downtime schema evolution

### Sharding Strategy Decision Matrix

| Criterion | Shared-Schema | Silo Model |
|-----------|---------------|------------|
| Tenant Count | 100+ tenants | <10 tenants |
| Schema Evolution | Single migration | Per-tenant migrations |
| Connection Pooling | Shared pools | Per-tenant pools |
| Isolation Level | Row-level (RLS) | Database-level |
| Operational Overhead | Low | High (linear with tenants) |
| Cost Profile | Low | High |

**Default**: Use Shared-Schema Multi-Tenancy for most scenarios. See [reference/sharding.md](reference/sharding.md) for detailed patterns.

## Domain-Specific Guidance

**Sharding**: Multi-tenant sharding, co-location, reference tables → See [reference/sharding.md](reference/sharding.md)

**Security**: Row Level Security, tenant isolation, agent SQL access → See [reference/security.md](reference/security.md)

**Event-Driven**: Transactional Outbox, CDC with Debezium, idempotency → See [reference/event-driven.md](reference/event-driven.md)

**Storage Lifecycle**: Tiered storage, partitioning, partition pruning → See [reference/storage-lifecycle.md](reference/storage-lifecycle.md)

**Schema Evolution**: Expand-and-Contract, zero-downtime migrations → See [reference/schema-evolution.md](reference/schema-evolution.md)

**Examples**: Real-world implementations → See [reference/examples.md](reference/examples.md)

## Execution Steps

### Step 1: Multi-Tenant Sharding

Implement Shared-Schema Multi-Tenancy with tenant_id distribution for horizontal scaling.

**Pattern**: tenant_id distribution column with co-location - See [reference/sharding.md](reference/sharding.md) for detailed implementation.

**Key Decision**: Use Shared-Schema for 100+ tenants. Co-locate related tables by same tenant_id.

**Best Practice**: Always distribute related tables by same tenant_id for local joins.

**Anti-Pattern**: ❌ Cross-shard joins (different distribution keys destroy performance). ❌ Missing co-location (forces network shuffling).

### Step 2: Row Level Security (RLS)

Enforce tenant isolation at database level using PostgreSQL RLS policies.

**Pattern**: Session-based tenant isolation with RLS policies - See [reference/security.md](reference/security.md) for implementation.

**Best Practice**: Always enable RLS policies. Application WHERE clauses are insufficient for agent SQL access.

**Anti-Pattern**: ❌ Application-only filtering (agents can bypass WHERE clauses via SQL injection).

### Step 3: Transactional Outbox

Ensure atomic event publishing via database transaction, eliminating dual write inconsistency.

**Pattern**: Outbox table with atomic transaction - See [reference/event-driven.md](reference/event-driven.md) for detailed implementation.

**Best Practice**: Single transaction for business entity update and outbox insert.

**Anti-Pattern**: ❌ Dual Write (separate commits cause inconsistency).

### Step 4: Change Data Capture (CDC)

Configure Debezium connector for log-based CDC, streaming outbox events to Kafka topics.

**Pattern**: Debezium Outbox Event Router - See [reference/event-driven.md](reference/event-driven.md) for connector configuration.

**Best Practice**: Use log-based CDC (Debezium) over polling for real-time event delivery.

**Anti-Pattern**: ❌ Polling outbox table (high latency, constant database load).

### Step 5: Idempotency

Implement processed_events table with idempotency key check, preventing duplicate event processing.

**Pattern**: Idempotency check with processed_events table - See [reference/event-driven.md](reference/event-driven.md) for implementation.

**Best Practice**: Check processed_events table before processing, insert event_id after in same transaction.

**Anti-Pattern**: ❌ Processing without idempotency checks (duplicate processing from at-least-once delivery).

### Step 6: Tiered Storage

Implement Hot-Warm-Cold partitioning using pg_partman for automatic partition management.

**Pattern**: Partitioned tables with pg_partman automation - See [reference/storage-lifecycle.md](reference/storage-lifecycle.md) for setup.

**Best Practice**: Always include time-bound WHERE clauses for partition pruning.

**Anti-Pattern**: ❌ Unrestricted queries across all partitions (causes timeouts and cost spikes).

### Step 7: Expand-and-Contract

Implement zero-downtime schema evolution using 5-phase migration pattern.

**Pattern**: 5-phase migration (Expand → Dual Write → Backfill → Switch Reads → Contract) - See [reference/schema-evolution.md](reference/schema-evolution.md) for detailed steps.

**Best Practice**: Use 5-phase migration for zero-downtime schema changes.

**Anti-Pattern**: ❌ Direct column rename/drop (requires downtime, breaks running applications).

## Common Patterns Quick Reference

1. **Shared-Schema Multi-Tenancy**: tenant_id distribution with co-location → See [reference/sharding.md](reference/sharding.md)
2. **Row Level Security**: Session-based tenant isolation → See [reference/security.md](reference/security.md)
3. **Transactional Outbox**: Atomic event publishing → See [reference/event-driven.md](reference/event-driven.md)
4. **Debezium CDC**: Log-based event streaming → See [reference/event-driven.md](reference/event-driven.md)
5. **Idempotency Pattern**: processed_events table check → See [reference/event-driven.md](reference/event-driven.md)
6. **Tiered Storage**: Hot-Warm-Cold partitioning → See [reference/storage-lifecycle.md](reference/storage-lifecycle.md)
7. **Expand-and-Contract**: Zero-downtime schema evolution → See [reference/schema-evolution.md](reference/schema-evolution.md)

## Best Practices Summary

### Sharding
- Always distribute related tables by same key (tenant_id)
- Co-locate related tables for local joins
- Use reference tables for global lookup data

### Security
- Always enable RLS policies
- Never rely solely on application WHERE clauses
- Set tenant context before queries

### Event-Driven
- Use log-based CDC (Debezium) over polling
- Always check processed_events before processing
- Implement idempotency for at-least-once delivery

### Storage Lifecycle
- Always include time-bound WHERE clauses for partition pruning
- Use pg_partman for automatic partition management
- Configure retention policies for old partitions

### Schema Evolution
- Use 5-phase migration (Expand → Dual Write → Backfill → Switch Reads → Contract)
- Never rename/drop columns directly
- Test migrations in staging first

## Workarounds Quick Reference

1. **Claim Check Pattern**: Large payload handling → See [reference/event-driven.md](reference/event-driven.md)
2. **Async Retrieval for Cold Data**: Historical data queries → See [reference/storage-lifecycle.md](reference/storage-lifecycle.md)
3. **Partitioned Outbox Retention**: Outbox table growth management → See [reference/event-driven.md](reference/event-driven.md)

## Anti-Patterns Quick Reference

1. **Dual Write**: Separate commits to database and broker → See [reference/event-driven.md](reference/event-driven.md)
2. **Cross-Shard Joins**: Different distribution keys → See [reference/sharding.md](reference/sharding.md)
3. **Fat Payload Outbox**: Large payloads in outbox table → See [reference/event-driven.md](reference/event-driven.md)
4. **Application-Only Filtering**: Missing RLS policies → See [reference/security.md](reference/security.md)
5. **Polling Outbox**: SELECT queries in loops → See [reference/event-driven.md](reference/event-driven.md)
6. **Missing Idempotency**: No duplicate prevention → See [reference/event-driven.md](reference/event-driven.md)
7. **Unrestricted Partition Queries**: Missing time-bound WHERE clauses → See [reference/storage-lifecycle.md](reference/storage-lifecycle.md)

## Real-World Examples

See [reference/examples.md](reference/examples.md) for minimal implementation examples:
- Multi-Tenant E-Commerce Platform
- Event-Driven Agent System

## Related Skills

- `implementing-resilient-agentic-architecture` - Cell-based architecture and static stability
- `implementing-kafka-production` - Kafka producer/consumer patterns
