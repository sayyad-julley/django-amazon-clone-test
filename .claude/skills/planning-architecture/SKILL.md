---
name: planning-architecture
description: Generates architecture plans and ADRs to guide system design.
---

# Architecture Planning Skill

This skill provides patterns for creating system architecture plans and documenting key architectural decisions using ADRs.

## Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Generating Architecture Plans](#generating-architecture-plans)
- [Writing ADRs](#writing-adrs)
- [Best Practices](#best-practices)
- [Related Skills](#related-skills)

## When to Use This Skill

Use this skill when:
- Designing a new service or system.
- Making significant architectural changes.
- Documenting technology decisions through ADRs.
- Planning system integrations or migrations.

## Generating Architecture Plans

Creates an architecture plan. The plan must follow the structured template defined in the progressive disclosure reference.

- **Reference Documentation**: [Architecture Plan Structure](reference.md)

### Key Sections in a Plan
- **Metadata**: Project identifiers and authorship.
- **Overview**: High-level goals and constraints.
- **Components**: Service-level breakdown (type, responsibility, interfaces).
- **Data Models**: Entity relationships and field definitions.
- **Security**: Authentication and authorization strategies.

## Writing ADRs

Creates an Architecture Decision Record (ADR) to document a key decision in a way that captures context and trade-offs.

### ADR Template Sections
1. **Title**: numbered kebab-case title.
2. **Status**: Proposed, Accepted, Deprecated, or Superseded.
3. **Context**: The problem and forces motivating the decision.
4. **Decision**: The specific response to the forces (active voice).
5. **Consequences**: Positive, negative, and trade-offs.

### Saving ADRs
Save ADRs in `docs/adr/` using the format: `NNNN-title-in-kebab-case.md`.

## Best Practices

1. **Start with requirements** - Understand the problem before design.
2. **Consider non-functionals** - Performance, scalability, security.
3. **Document trade-offs** - Use the ADR pattern for transparency.
4. **Plan for evolution** - System designs change; avoid rigidity.

## Related Skills

- `executing-code`
- `integrating-linear`
- `customizing-implementing-kong-gateway`
