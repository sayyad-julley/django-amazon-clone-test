---
name: implementing-resilient-agentic-architecture
description: Implements resilient agentic AI architectures by applying proven patterns (SAGA orchestration with compensation events, CDC pipelines for real-time context, circuit breakers for LLM calls, schema contracts with Pydantic), following best practices (orchestration over choreography, external workers for Python agents, declarative rollback via BPMN, CDC over batch ETL), implementing workarounds (non-blocking Kafka consumers, internal queues for slow processing, idempotency keys), and avoiding anti-patterns (chatty sagas, synchronous blocks, implicit compensations, pinball effect, god processes). Use when building production-grade AI agents, orchestrating distributed workflows, implementing event-driven agent communication, managing probabilistic systems with deterministic guarantees, or coordinating multi-step agent actions.
version: 1.0.0
dependencies:
  - org.flowable:flowable-spring-boot-starter>=7.0.1
  - apache-kafka>=3.0.0
  - debezium-connector-postgres>=2.0.0
  - pydantic>=2.0.0
  - confluent-kafka>=2.0.0
---

# Implementing Resilient Agentic Architecture

## Overview

Bridges deterministic infrastructure with probabilistic LLM reasoning. Imposes reliability, consistency, and auditability constraints through SAGA patterns, CDC pipelines, circuit breakers, schema contracts, and orchestration engines.

## When to Use

Use this skill when:
- Building production-grade AI agents requiring reliability guarantees
- Orchestrating distributed workflows across multiple microservices
- Implementing event-driven agent communication patterns
- Managing probabilistic systems with deterministic infrastructure
- Coordinating multi-step agent actions with compensation requirements
- Integrating AI agents with existing enterprise systems
- Implementing real-time context synchronization for agent memory

**Input format**: Agent requirements, microservice architecture, database schemas, event streaming infrastructure, orchestration engine access

**Expected output**: Production-ready agentic architecture following proven patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- Understanding of distributed systems patterns (SAGA, Event Sourcing, CQRS)
- Access to orchestration engine (Flowable, Temporal, or similar)
- Event streaming infrastructure (Kafka, Pulsar, or similar)
- Database with CDC capabilities (PostgreSQL, MySQL with binlog)
- Python runtime for agent implementation
- Schema registry for contract management (optional but recommended)

## Quick Start

### Key Patterns Summary

1. **SAGA Orchestration**: Compensation boundary events with declarative rollback
2. **CDC Pipeline**: Debezium → Kafka → Flowable Event Registry → Vector Store
3. **External Worker**: Python agents poll Flowable REST API for jobs
4. **Circuit Breaker**: State machine (Closed/Open/Half-Open) for LLM calls
5. **Schema Validation**: Pydantic models for agent output validation
6. **Non-Blocking Consumer**: Async/await Kafka consumers for agent communication
7. **Idempotency Keys**: Deterministic UUIDs for tool call deduplication

### Orchestration Decision Matrix

| Pattern | Description | Flowable Implementation | Best For |
|---------|-------------|------------------------|----------|
| Sequential | Step A → Step B. If fail, stop. | BPMN Sequence Flow | Strict compliance workflows |
| Parallel (Fan-out) | Run Agents A, B, C concurrently | BPMN Parallel Gateway or CMMN Stages | Research agents (search web, check docs) |
| Human-in-the-Loop | Agent pauses and waits for approval | User Task (assigned to human group) | High-risk actions (funds transfer) |
| Adaptive / Goal-Driven | Agent decides what to do next | CMMN Plan Items with Sentry conditions | Complex case management, Support Agents |

**Default**: Use orchestration over choreography for agentic systems. See [reference/execution-steps.md](reference/execution-steps.md) for detailed patterns.

## Domain-Specific Guidance

**Execution Steps**: SAGA patterns, CDC pipelines, event-driven communication, resilience, contracts, orchestration, observability → See [reference/execution-steps.md](reference/execution-steps.md)

**Common Patterns**: SAGA orchestration, CDC, external workers, circuit breakers, schema validation, non-blocking consumers → See [reference/patterns.md](reference/patterns.md)

**Best Practices**: Orchestration over choreography, external workers, compensation events, CDC over batch, schema validation, circuit breakers, idempotency → See [reference/best-practices.md](reference/best-practices.md)

**Workarounds**: Non-blocking consumer loops, internal queues, composite keys → See [reference/workarounds.md](reference/workarounds.md)

**Anti-Patterns**: Chatty saga, synchronous blocks, implicit compensations, pinball effect, god process, no schema validation, batch ETL → See [reference/anti-patterns.md](reference/anti-patterns.md)

**Examples**: Real-world implementations → See [reference/examples.md](reference/examples.md)

## Execution Steps

### Step 1: SAGA Pattern Implementation

SAGA replaces 2PC with sequences of local transactions for eventual consistency. Use orchestration over choreography. Attach compensation boundary events to tasks for declarative rollback.

**Pattern**: Orchestration with compensation events - See [reference/execution-steps.md](reference/execution-steps.md#step-1-saga-pattern-implementation) for detailed implementation.

**Key Decision**: Use orchestration (centralized coordinator) over choreography (decentralized events) for agentic systems.

**Best Practice**: Always use external workers for long-running LLM calls. Never use synchronous JavaDelegates.

**Anti-Pattern**: ❌ Choreography causes "Pinball Effect". ❌ Synchronous blocks kill throughput.

**Templates**: See `templates/flowable-saga-bpmn.template` and `templates/python-external-worker.template`

### Step 2: CDC Pipeline Architecture

CDC treats database transaction logs as event streams, enabling real-time agent reactions. Configure Debezium connector and Flowable Event Registry.

**Pattern**: Source → Connector → Transport → Event Registry → Sink - See [reference/execution-steps.md](reference/execution-steps.md#step-2-cdc-pipeline-architecture) for detailed implementation.

**Best Practice**: Use CDC instead of batch ETL jobs for agent memory. Stream only deltas to vector store.

**Anti-Pattern**: ❌ Batch ETL for agent memory causes data staleness.

**Templates**: See `templates/debezium-source-config.template` and `templates/flowable-event-registry.template`

### Step 3: Event-Driven Agent Communication

Agents communicate asynchronously via Kafka. Use non-blocking consumer loops to prevent blocking heartbeat threads.

**Pattern**: Non-blocking consumer with async/await - See [reference/execution-steps.md](reference/execution-steps.md#step-3-event-driven-agent-communication) for detailed implementation.

**Best Practice**: Never block Kafka consumer thread with slow operations. Use async processing.

**Anti-Pattern**: ❌ Blocking consumer thread prevents offset commits and increases lag.

**Template**: See `templates/kafka-non-blocking-consumer.template`

### Step 4: Resilience Patterns

Implement circuit breakers for external LLM API calls to prevent cascading failures and control costs.

**Pattern**: Circuit breaker state machine (Closed/Open/Half-Open) - See [reference/execution-steps.md](reference/execution-steps.md#step-4-resilience-patterns) for detailed implementation.

**Best Practice**: Implement circuit breakers for all external LLM API calls. Configure appropriate thresholds.

**Anti-Pattern**: ❌ No failure handling allows cascading failures.

**Template**: See `templates/circuit-breaker-python.template`

### Step 5: Contract Layer

Validate all agent outputs with Pydantic schemas. Use Schema Registry for centralized schema management.

**Pattern**: Schema validation with Pydantic - See [reference/execution-steps.md](reference/execution-steps.md#step-5-contract-layer) for detailed implementation.

**Best Practice**: Always validate agent outputs with schemas. Use Pydantic for Python agents.

**Anti-Pattern**: ❌ No schema validation causes production failures.

**Template**: See `templates/pydantic-schema-validation.template`

### Step 6: Flowable Orchestration Patterns

Use BPMN for deterministic workflows, CMMN for adaptive goal-driven agents. Implement external worker polling pattern.

**Pattern**: External worker polling with REST API - See [reference/execution-steps.md](reference/execution-steps.md#step-6-flowable-orchestration-patterns) for detailed implementation.

**Best Practice**: Use appropriate polling intervals (1-5 seconds). Handle connection errors gracefully.

**Anti-Pattern**: ❌ God Process: Single BPMN with 50+ steps (unmaintainable).

**Template**: See `templates/python-external-worker.template`

### Step 7: Observability and Governance

Define agent-specific SLOs (Goal Completion Rate, Turn Efficiency, Hallucination Rate). Use idempotency keys for all tool calls.

**Pattern**: Agent SLOs and idempotency keys - See [reference/execution-steps.md](reference/execution-steps.md#step-7-observability-and-governance) for detailed implementation.

**Best Practice**: Always use idempotency keys for tool calls. Generate keys deterministically.

**Anti-Pattern**: ❌ No idempotency causes double-charging and duplicate bookings.

## Common Patterns Quick Reference

1. **SAGA Orchestration with Compensation**: Declarative rollback via BPMN → See [reference/patterns.md](reference/patterns.md#pattern-1-saga-orchestration-with-compensation)
2. **CDC for Real-Time Context**: Stream database changes to vector stores → See [reference/patterns.md](reference/patterns.md#pattern-2-cdc-for-real-time-context)
3. **External Worker for Python Integration**: REST API polling pattern → See [reference/patterns.md](reference/patterns.md#pattern-3-external-worker-for-python-integration)
4. **Circuit Breaker for LLM Calls**: Failure protection and cost control → See [reference/patterns.md](reference/patterns.md#pattern-4-circuit-breaker-for-llm-calls)
5. **Schema Validation with Pydantic**: Self-correction loops → See [reference/patterns.md](reference/patterns.md#pattern-5-schema-validation-with-pydantic)
6. **Non-Blocking Kafka Consumer**: Async/await pattern → See [reference/patterns.md](reference/patterns.md#pattern-6-non-blocking-kafka-consumer)

## Best Practices Summary

### Orchestration
- Use orchestration over choreography for agentic systems
- Always use external workers for long-running LLM calls
- Implement compensation events, not manual rollback logic

### Event-Driven
- Use CDC instead of batch jobs for agent memory
- Never block Kafka consumer thread with slow operations
- Use internal queues when processing is slower than consumption rate

### Reliability
- Validate all agent outputs with schemas
- Implement circuit breakers for external API calls
- Use idempotency keys for all tool calls

### Workflow Design
- Group cognitive steps into larger units of work
- Break workflows into modular sub-processes
- Monitor agent-specific SLOs beyond traditional metrics

**Detailed practices**: See [reference/best-practices.md](reference/best-practices.md)

## Workarounds Quick Reference

1. **Non-Blocking Consumer Loop**: For Kafka consumer lag mitigation → See [reference/workarounds.md](reference/workarounds.md#workaround-1-non-blocking-consumer-loop-for-python-agents)
2. **Internal Queue for Slow Processing**: When processing is slower than consumption → See [reference/workarounds.md](reference/workarounds.md#workaround-2-internal-queue-for-slow-processing)
3. **Composite Keys for Low-Cardinality Partitioning**: For hotspotting mitigation → See [reference/workarounds.md](reference/workarounds.md#workaround-3-composite-keys-for-low-cardinality-partitioning)

## Anti-Patterns Quick Reference

1. **Chatty Saga**: Fine-grained transactions for every agent thought → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-1-chatty-saga)
2. **Synchronous Block**: Blocking LLM calls in Flowable threads → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-2-synchronous-block)
3. **Implicit Compensations**: LLM-generated rollback logic → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-3-implicit-compensations)
4. **Pinball Effect**: Choreography for agent workflows → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-4-pinball-effect-choreography)
5. **God Process**: Monolithic BPMN with 50+ steps → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-5-god-process)
6. **No Schema Validation**: Relying on prompt engineering alone → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-6-no-schema-validation)
7. **Batch ETL for Agent Memory**: Nightly batch jobs instead of CDC → See [reference/anti-patterns.md](reference/anti-patterns.md#anti-pattern-7-batch-etl-for-agent-memory)

## Real-World Examples

See [reference/examples.md](reference/examples.md) for minimal implementation examples:
- Flowable SAGA with Compensation
- CDC Pipeline with Debezium + Flowable Event Registry

## Related Skills

- `implementing-flowable-7-spring-boot-3`: Flowable orchestration engine integration
- `implementing-kafka-production`: Kafka event streaming patterns
- `implementing-spring-boot-3.2.5-java17`: Spring Boot microservices foundation
