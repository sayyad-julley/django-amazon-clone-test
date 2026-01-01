---
name: implementing-platform-engineering-strategy
description: Implements Platform Engineering Strategy by applying patterns (Bridge Tenancy Model, Tech Radar governance, PBC composability, Standard Webhooks, MCP agentic interfaces, Permit.io Policy-as-Code), following best practices (Wardley Mapping, ADRs, MACH architecture, Circuit Breakers, Tenant Context Objects), implementing workarounds (Tier-Based Migration, PDP fallback strategies, Partial Evaluation), and avoiding anti-patterns (Universal Silo, Leaky Pools, Distributed Monolith, Component Sprawl, Custom-Building Commodities). Use when designing multi-tenant platforms, implementing governance frameworks, building composable architectures, creating extensible ecosystems, integrating AI agents via MCP, or establishing Policy-as-Code enforcement.
version: 1.0.0
---

# Implementing Platform Engineering Strategy

## Overview

Platform Engineering Strategy provides actionable guidance for building scalable, governed, composable platforms with agentic extensibility. The strategy employs Wardley Mapping for strategic decision-making, balancing cost and isolation through tenancy models, preventing component sprawl via governance, enabling composability through Packaged Business Capabilities (PBCs), and integrating AI agents via Model Context Protocol (MCP). Policy enforcement uses Permit.io for Policy-as-Code with sidecar PDP architecture.

## When to Use

Use this skill when:
- Designing multi-tenant platforms requiring strategic scalability decisions
- Implementing governance frameworks to prevent component sprawl
- Building composable architectures using PBCs
- Creating extensible ecosystems with webhooks and plugins
- Integrating AI agents via MCP for autonomous operations
- Establishing Policy-as-Code enforcement with Permit.io
- Making Buy vs Build decisions for platform capabilities

**Input format**: Platform requirements (isolation needs, compliance requirements, scale expectations), existing infrastructure, business capability map

**Expected output**: Production-ready platform architecture following proven patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- Understanding of cloud-native architecture (Kubernetes, microservices)
- Access to platform infrastructure (compute, storage, networking)
- Understanding of business capabilities and domain boundaries
- Policy and compliance requirements documented
- Access to IDP tools (Backstage, Port) if implementing governance
- Permit.io account for Policy-as-Code (if implementing authorization)

## Quick Start

### Key Patterns Summary

1. **Bridge Tenancy Model**: Pooled compute with siloed storage (default choice)
2. **Tech Radar Governance**: Four-ring structure (Adopt, Trial, Assess, Hold)
3. **PBC Composability**: Experience API + Event Interface + Data Schema
4. **Standard Webhooks**: HMAC signatures + timestamp + idempotency
5. **MCP Agentic**: Tools, Resources, Prompts with Circuit Breakers
6. **Permit.io Policy**: Sidecar PDP for sub-millisecond authorization
7. **Buy vs Build**: Core vs Context framework

### Tenancy Model Decision Matrix

| Criterion | Silo Model | Bridge Model | Pool Model |
|----------|------------|--------------|------------|
| Target Customer | Enterprise/Gov | Mid-Market | SMB/Freemium |
| Isolation Boundary | Network/Infra | Database Schema | Application Logic |
| Cost Profile | High | Medium | Low |
| Compliance | Strict (HIPAA) | Moderate (GDPR) | Standard |
| Performance SLA | Guaranteed | Burstable | Best Effort |

**Default**: Use Bridge Model for most scenarios. See [reference/scalability.md](reference/scalability.md) for detailed patterns.

## Domain-Specific Guidance

**Scalability**: Tenancy models, tenant context, tier-based migration → See [reference/scalability.md](reference/scalability.md)

**Governance**: Tech Radar, ADRs, automated EA ingestion → See [reference/governance.md](reference/governance.md)

**Composability**: PBCs, MACH architecture, event-driven communication → See [reference/composability.md](reference/composability.md)

**Extensibility**: Standard Webhooks, WASM sandbox, exponential backoff → See [reference/extensibility.md](reference/extensibility.md)

**Agentic**: MCP Server, Circuit Breakers, HITL patterns → See [reference/agentic.md](reference/agentic.md)

**Policy**: Permit.io RBAC/ReBAC, sidecar PDP, tenant isolation → See [reference/policy.md](reference/policy.md)

**De-duplication**: Buy vs Build, Core vs Context, Golden Services → See [reference/deduplication.md](reference/deduplication.md)

**Examples**: Real-world implementations → See [reference/examples.md](reference/examples.md)

## Execution Steps

### Step 1: Strategic Scalability - Tenancy Model Selection

Select tenancy model based on isolation requirements, cost constraints, and compliance needs.

**Pattern**: Bridge Model (Pooled Compute, Siloed Storage) - See [reference/scalability.md](reference/scalability.md) for detailed implementation.

**Key Decision**: Use decision matrix above. Default to Bridge Model unless strict compliance requires Silo.

**Best Practice**: Implement Tier-Based Migration capability to move tenants between models as they grow.

**Anti-Pattern**: ❌ Universal Silo (defaulting to Silo for everyone). ❌ Leaky Pools (missing Row Level Security).

### Step 2: Governance - Tech Radar Implementation

Implement Tech Radar to visualize and manage technology portfolio, preventing component sprawl.

**Pattern**: Four-ring structure (Adopt, Trial, Assess, Hold) - See [reference/governance.md](reference/governance.md) for structure and automation.

**Best Practice**: Link "Adopt" technologies to IDP Scaffolder Templates. Automate EA ingestion from catalog-info.yaml.

**Anti-Pattern**: ❌ Stale radar (unchanged for 6+ months). ❌ Component Sprawl (no governance).

### Step 3: Governance - Architecture Decision Records

Document architectural decisions to prevent tribal knowledge silos.

**Pattern**: ADR format (Context, Decision, Status, Consequences) - See [reference/governance.md](reference/governance.md) for template.

**Best Practice**: Version control ADRs in `/docs/adr` alongside code. Review quarterly.

**Anti-Pattern**: ❌ Tribal Knowledge (decisions only in people's heads).

### Step 4: Composability - Packaged Business Capabilities

Organize platform around PBCs for functional autonomy and business alignment.

**Pattern**: PBC structure (Experience API, Event Interface, Data Schema, Metadata Catalog) - See [reference/composability.md](reference/composability.md) for details.

**Best Practice**: Align with MACH (Microservices, API-first, Cloud-native, Headless). Enforce PBC autonomy (no shared databases).

**Anti-Pattern**: ❌ Distributed Monolith (PBCs share database). ❌ Component Spaghetti (overlapping PBCs).

### Step 5: Extensibility - Standard Webhooks

Implement Standard Webhooks specification for secure, reliable event delivery.

**Pattern**: HMAC signatures, Timestamp replay protection, Idempotency - See [reference/extensibility.md](reference/extensibility.md) for verification implementation.

**Best Practice**: Exponential backoff retry (5s, 30s, 5m, 1h). Dead-letter after 72 hours.

**Anti-Pattern**: ❌ Fire-and-Forget (no reliability guarantees).

### Step 6: Extensibility - WASM Sandbox

Use WebAssembly for synchronous extensibility with security isolation.

**Pattern**: Capability-based security (WASI) - See [reference/extensibility.md](reference/extensibility.md) for plugin structure.

**Best Practice**: Restricted environment (no network/FS access by default). Grant capabilities explicitly via WASI.

**Anti-Pattern**: ❌ Trusting untrusted code execution without sandboxing.

### Step 7: Agentic Integration - MCP Server

Implement MCP server to expose platform capabilities to AI agents.

**Pattern**: Tools, Resources, Prompts structure with Circuit Breakers - See [reference/agentic.md](reference/agentic.md) for implementation.

**Best Practice**: Wrap all MCP tools in Circuit Breakers. Sanitize outputs (mask PII/secrets). Require HITL for destructive actions.

**Anti-Pattern**: ❌ Unprotected agent interfaces (no Circuit Breakers or HITL).

### Step 8: Policy as Code - Permit.io Implementation

Enforce governance and isolation programmatically using Permit.io with sidecar PDP architecture.

**Pattern**: Sidecar PDP for sub-millisecond authorization, RBAC/ReBAC policies - See [reference/policy.md](reference/policy.md) for detailed patterns.

**Best Practice**: Deploy PDP as sidecar per service. Use Admin SDK for tenant/user sync. Implement fallback to deny on PDP unavailable.

**Anti-Pattern**: ❌ Direct API calls from hot path. ❌ Hardcoded permissions. ❌ Global role assignments.

### Step 9: De-duplication - Buy vs Build

Apply Core vs Context framework to prevent redundant commodity implementations.

**Pattern**: Core vs Context framework - See [reference/deduplication.md](reference/deduplication.md) for decision matrix.

**Best Practice**: Create Golden Services (Facade Pattern) around bought capabilities. Enables vendor swapping without breaking applications.

**Anti-Pattern**: ❌ Custom-Building Commodities (NIH syndrome for commodity services).

## Common Patterns Quick Reference

1. **Bridge Tenancy Model**: Pooled compute + Siloed storage → See [reference/scalability.md](reference/scalability.md)
2. **Tenant Context Object**: Strongly-typed tenant context injection → See [reference/scalability.md](reference/scalability.md)
3. **Tech Radar Governance**: Four-ring structure with automated ingestion → See [reference/governance.md](reference/governance.md)
4. **PBC Structure**: Experience API + Event Interface + Data Schema → See [reference/composability.md](reference/composability.md)
5. **Standard Webhooks**: HMAC + Timestamp + Idempotency → See [reference/extensibility.md](reference/extensibility.md)
6. **MCP Circuit Breaker**: Agent resilience pattern → See [reference/agentic.md](reference/agentic.md)
7. **Permit.io Tenant Isolation**: RBAC/ReBAC policy for multi-tenant security → See [reference/policy.md](reference/policy.md)

## Best Practices Summary

### Scalability
- Use Bridge Model as default (cost/isolation balance)
- Implement Tier-Based Migration capability
- Use Tenant Context Object (never raw tenant_id)

### Governance
- Link Tech Radar to IDP Scaffolder Templates
- Automate EA ingestion from catalog-info.yaml
- Version control ADRs in code repository

### Composability
- Enforce PBC autonomy (no shared databases)
- Use Event-Driven communication (async)
- Maintain Capability Map in Ardoq/LeanIX

### Extensibility
- Always verify webhook signatures (HMAC-SHA256)
- Use WASM for synchronous extensibility
- Implement exponential backoff for webhooks

### Agentic
- Wrap all MCP tools in Circuit Breakers
- Sanitize tool outputs (mask PII/secrets)
- Require HITL for destructive actions

### Policy
- Deploy Permit.io PDP as sidecar per service
- Use Admin SDK for tenant/user sync
- Implement fallback to deny on PDP unavailable

### De-duplication
- Buy Context capabilities (Identity, Notifications, Billing)
- Build Core capabilities (Pricing Engine, Fraud Detection)
- Create Golden Services (Facade Pattern)

## Workarounds Quick Reference

1. **Tier-Based Migration**: Moving tenants between tenancy models → See [reference/scalability.md](reference/scalability.md)
2. **PDP Fallback**: Fallback to deny on PDP unavailable → See [reference/policy.md](reference/policy.md)
3. **PDP Proximity Trade-offs**: Sidecar vs DaemonSet deployment → See [reference/policy.md](reference/policy.md)
4. **Internal Queue**: For consumer lag mitigation → See [reference/extensibility.md](reference/extensibility.md)

## Anti-Patterns Quick Reference

1. **Universal Silo**: Defaulting to Silo for everyone → See [reference/scalability.md](reference/scalability.md)
2. **Leaky Pools**: Missing RLS in Pool model → See [reference/scalability.md](reference/scalability.md)
3. **Distributed Monolith**: PBCs sharing databases → See [reference/composability.md](reference/composability.md)
4. **Component Sprawl**: No governance leading to technology chaos → See [reference/governance.md](reference/governance.md)
5. **Custom-Building Commodities**: NIH syndrome for commodity services → See [reference/deduplication.md](reference/deduplication.md)
6. **Fire-and-Forget Webhooks**: No reliability guarantees → See [reference/extensibility.md](reference/extensibility.md)
7. **Unprotected Agent Interfaces**: No Circuit Breakers or HITL → See [reference/agentic.md](reference/agentic.md)
8. **Hardcoded Permissions**: Authorization logic in code → See [reference/policy.md](reference/policy.md)

## Real-World Examples

See [reference/examples.md](reference/examples.md) for minimal implementation examples:
- Bridge Model Implementation
- MCP Server with Circuit Breaker

## Related Skills

- `implementing-permitio-authorization` - Detailed Permit.io authorization patterns
- `implementing-resilient-agentic-architecture` - Cell-based architecture and static stability

