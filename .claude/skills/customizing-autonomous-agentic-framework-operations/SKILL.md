---
name: autonomous-agentic-framework-operations
description: Provides operational techniques for autonomous agentic frameworks including prompt caching configuration (cache_control parameter, 90% cost reduction), batch processing (50% cost savings), cost optimization across subagents, and memory checkpointing/rollback patterns. Use during SDLC orchestration workflow phases (Research, Plan, Implement) when optimizing agent costs, configuring cache_control for subagents, implementing file checkpointing, or enhancing existing CostTracker usage.
version: 1.0.0
dependencies: []
---

# Autonomous Agentic Framework Operations

## Overview

Operational techniques for optimizing, orchestrating, and governing autonomous agentic frameworks built on the Claude Agent SDK. Focuses on cost reduction, context management, and reliability patterns applicable during SDLC orchestration workflows.

## Orchestration Workflow Integration

Use these techniques during RPI (Research-Plan-Implement) workflow phases:

**Research Phase:**
- Configure prompt caching (`cache_control`) for research subagents
- Optimize cost tracking across parallel research subagents

**Plan Phase:**
- Plan cost optimization strategies
- Design checkpointing strategy for implementation phase

**Implement Phase:**
- Use memory checkpointing before destructive operations
- Implement rollback patterns on failures

## Quick Reference

| Technique | When to Use | Cost Impact | Link |
|-----------|-------------|------------|------|
| Prompt Caching | Long-running sessions, parallel subagents | 90% input cost reduction | [Prompt Caching Guide](resources/prompt-caching-guide.md) |
| Batch Processing | Non-interactive bulk operations | 50% cost reduction | [Batch Processing Patterns](resources/batch-processing-patterns.md) |
| Cost Optimization | Multi-agent workflows, budget enforcement | Variable | [Cost Optimization](resources/cost-optimization.md) |
| Memory Checkpointing | Before destructive operations, test failures | Prevents data loss | [Memory Checkpointing](resources/memory-checkpointing.md) |

## Core Techniques

### Prompt Caching Configuration

Configure `cache_control` parameter for three-tier caching strategy:

- **Foundational**: Tool definitions and core system prompts (most stable)
- **Contextual**: Project-specific docs and directory structures
- **Episodic**: Conversation history and tool results (updated per turn)

**Decision Tree:**
- TTL selection: 5-minute for interactive sessions, 1-hour for background agents
- Breakpoint placement: After system message, after file context, after each turn

See [Prompt Caching Guide](resources/prompt-caching-guide.md) for implementation details.

### Batch Processing for Scale

Use Message Batches API for non-interactive operations:

- Up to 100,000 requests per batch
- 50% cost reduction vs standard API
- Map-Reduce pattern for parallel subagent execution

See [Batch Processing Patterns](resources/batch-processing-patterns.md) for orchestration patterns.

### Cost Optimization

Enhance existing CostTracker usage across subagents:

- Cost aggregation patterns
- Budget enforcement strategies
- Token economics in RPI workflow

See [Cost Optimization](resources/cost-optimization.md) for advanced patterns.

### Memory Checkpointing

File checkpointing and rollback capabilities:

- Checkpoint creation before destructive operations
- Rollback on test failures
- Integration with `.sdlc/memories/` storage

See [Memory Checkpointing](resources/memory-checkpointing.md) for rollback patterns.

## Integration Patterns

**Research Phase Optimization:**
```python
# Configure cache_control for research subagents
options = ClaudeAgentOptions(
    cache_control={
        "type": "ephemeral",
        "ttl": "5m"  # 5-minute TTL for interactive research
    }
)
```

**Implement Phase Safety:**
```python
# Checkpoint before destructive operations
checkpoint_id = create_checkpoint(target_files)
try:
    execute_implementation()
except TestFailure:
    rollback_to_checkpoint(checkpoint_id)
```

## Safety Considerations

- **Budget Enforcement**: Always set budget limits when spawning subagents
- **Checkpoint Before Writes**: Create checkpoints before destructive file operations
- **Cache TTL Selection**: Use 1-hour TTL only for background agents, not interactive sessions
- **Cost Aggregation**: Track costs across all subagents to prevent budget overruns

## Workflow Checklists

### Research Phase Checklist

- [ ] Configure `cache_control` with three-tier breakpoints
- [ ] Set appropriate TTL (5-minute for interactive, 1-hour for background)
- [ ] Enable cost tracking for research subagents
- [ ] Aggregate costs across parallel research tasks

### Plan Phase Checklist

- [ ] Review cost estimates from research phase
- [ ] Plan checkpointing strategy for implementation
- [ ] Set budget limits for implementation phase
- [ ] Design rollback triggers (test failures, errors)

### Implement Phase Checklist

- [ ] Create checkpoint before first file modification
- [ ] Monitor cost tracker for budget limits
- [ ] Rollback on test failures
- [ ] Verify checkpoint restoration after rollback

## Detailed Resources

| Resource | Description |
|----------|-------------|
| [Prompt Caching Guide](resources/prompt-caching-guide.md) | Three-tier caching strategy, TTL selection, token economics |
| [Batch Processing Patterns](resources/batch-processing-patterns.md) | Message Batches API, Map-Reduce patterns, polling mechanisms |
| [Cost Optimization](resources/cost-optimization.md) | CostTracker enhancement, aggregation patterns, budget enforcement |
| [Memory Checkpointing](resources/memory-checkpointing.md) | File snapshots, rollback strategies, RPI integration |
| [Orchestration Integration](resources/orchestration-integration.md) | RPI workflow integration, SessionContext patterns, subagent spawning |

## Templates

- [Cache Control Configuration](templates/cache-control-config.template) - Three-tier breakpoint examples
- [Batch Orchestrator](templates/batch-orchestrator.template) - Polling and result synthesis patterns
- [Checkpoint Rollback](templates/checkpoint-rollback.template) - File snapshot and restoration patterns

