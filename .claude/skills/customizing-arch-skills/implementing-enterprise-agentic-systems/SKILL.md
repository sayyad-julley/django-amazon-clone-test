---
name: implementing-enterprise-agentic-systems
description: Implements enterprise-grade agentic systems by applying proven patterns (ReAct, Reflection, Orchestrator-Workers, Planning), following best practices (Clean Architecture, idempotency, retry with backoff, circuit breakers, guardrails, Zero Trust identity), implementing workarounds (idempotency keys, exponential backoff with jitter, circuit breaker state machines, guardrails middleware), and avoiding anti-patterns (God Agent context overload, infinite ReAct loops, hallucination cascades, open loop execution). Use when building production-ready agents, implementing reliability patterns, designing multi-agent systems, or requiring deterministic reliability around probabilistic agents.
version: 1.0.0
category: design
dependencies:
  - python>=3.9
  - typescript>=5.0
---

# Implementing Enterprise-Grade Agentic Systems

## Overview

Implements production-ready agentic systems using Clean Architecture, proven cognitive patterns, and reliability primitives. Bridges the deterministic-probabilistic paradox by constructing deterministic engineering primitives around non-deterministic cognitive cores. Provides patterns for reasoning loops (ReAct, Reflection, Planning), multi-agent coordination (Orchestrator-Workers), and reliability mechanisms (idempotency, retry, circuit breakers, guardrails).

## When to Use

Use this skill when:
- Building production-ready autonomous agents requiring deterministic reliability
- Implementing multi-agent systems with coordination requirements
- Designing agent architectures with Clean Architecture boundaries
- Requiring resilience patterns (idempotency, retry, circuit breakers)
- Building systems requiring Zero Trust security (SPIFFE/SPIRE)
- Implementing Model Context Protocol (MCP) integrations
- Avoiding common agent failure modes (context overload, infinite loops, hallucination cascades)

**Input format**: Agent requirements, task complexity, reliability targets, security constraints

**Expected output**: Production-ready agent architecture with patterns applied, best practices followed, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill:
- Understanding of LLM capabilities and limitations
- Knowledge of distributed systems patterns
- Familiarity with Clean Architecture principles
- Access to LLM providers (OpenAI, Anthropic, local models)
- Python 3.9+ or TypeScript 5.0+ for implementations

## Execution Steps

### Step 1: Clean Architecture Setup

Organize system into concentric circles ensuring agent reasoning remains independent of frameworks.

**Domain Layer (Entities)**: Define Persona, Goals, and Reasoning Strategy. Must be framework-agnostic (no LangChain, PydanticAI, or custom loop dependencies). Encodes business rules as invariants (e.g., "Must cite sources", "Cannot authorize transactions over $10,000").

**Use Case Layer (Interactors)**: Orchestrates workflows (ReAct/Plan-and-Execute loops). Manages task lifecycle: retrieve request, initialize agent, manage conversation history, persist artifacts.

**Interface Adapters**: 
- **LLM Adapters**: Abstract model providers (OpenAI, Anthropic, local LLaMA). Enables model switching without business logic changes.
- **Tool Adapters**: Convert agent intent (JSON) into concrete API calls. Handle serialization of tool outputs back to natural language.

**Frameworks and Drivers**: Concrete implementations (FastAPI, PostgreSQL/pgvector, LangGraph, AutoGen). Pushed to edge for testability.

**Critical Practices**:
- Domain layer must not import from infrastructure
- Use dependency injection for external dependencies
- Framework-agnostic domain enables unit testing with mocked LLM adapters

### Step 2: Pattern Selection

Select appropriate cognitive pattern based on task characteristics:

**ReAct Pattern**: Use for dynamic information gathering where path is unknown upfront. Requires TTL/max iterations (mandatory: 10 steps).

**Planning Pattern**: Use for long-horizon tasks requiring multi-step coordination. Generate DAG before execution, allow replanning.

**Reflection Pattern**: Use for high-accuracy requirements. Generate → Critique → Refine loop with specialized Critic agent.

**Orchestrator-Workers Pattern**: Use for multi-domain tasks requiring specialization. Router delegates to workers with <10 tools each, narrow context.

**Decision Tree**:
- Unknown path + dynamic info → ReAct
- Long-horizon + structured steps → Planning
- High accuracy + quality critical → Reflection
- Multi-domain + specialization → Orchestrator-Workers

### Step 3: Reliability Primitives

Implement deterministic reliability around probabilistic agents:

**Idempotency**: Every state-changing tool call includes unique Idempotency-Key (UUID or hash). Server-side caching returns cached response for duplicate keys.

**Retry with Exponential Backoff**: `sleep = min(cap, base * 2^attempt) + random()`. Jitter desynchronizes multiple agents retrying simultaneously.

**Circuit Breakers**: Closed → Open → Half-Open state machine. After N failures, block calls and return immediate error. Half-open allows probe request.

**Guardrails**: Input/output interception layers. Scan for PII, prompt injection, hallucinated URLs, toxic content. Tripwire detection halts request.

## Common Patterns

### Pattern 1: ReAct (Reason + Act)

Decouples reasoning from execution, forcing agent to articulate Thought before Action, then observe output.

**Implementation**: Thought → Action → Observation loop. Agent analyzes state, determines next step, selects tool with parameters, receives observation, repeats.

**When to Use**: Dynamic information gathering, unknown path, research tasks, exploratory queries.

**Template**: See `templates/react-pattern.template` for loop structure.

**Best Practice**: Mandatory TTL or maximum iteration count (10 steps). Implement loop detection for duplicate consecutive tool calls.

**Trade-offs**: Can loop indefinitely without guardrails. Higher latency than direct execution. Medium complexity, high cost.

### Pattern 2: Reflection and Self-Correction

Forces System 2 (slow, deliberative) process by introducing critique step after generation.

**Implementation**: Generate → Reflect/Critique → Refine. Agent produces draft, specialized Critic reviews against constraints (compiles? citations valid?), agent uses critique for improved version.

**When to Use**: High accuracy requirements, code generation, legal drafting, quality-critical outputs.

**Template**: See `templates/reflection-pattern.template` for workflow structure.

**Best Practice**: Use specialized Critic agent for validation. In code generation, Tester Agent executes script, feeds stderr back to Coder Agent for reflection.

**Trade-offs**: Slower (2x-3x calls). Significantly higher cost. Medium complexity, very high cost.

### Pattern 3: Orchestrator-Workers (Swarm)

Decomposes high-level goal into sub-tasks delegated to specialized workers, acting as cognitive load balancer.

**Implementation**: Router/Orchestrator analyzes user intent, routes to specialist (e.g., "billing query → BillingAgent"). Workers have narrow tools and context. Orchestrator synthesizes results.

**When to Use**: Multi-domain tasks, enterprise workflows, specialization requirements, context overload scenarios.

**Template**: See `templates/orchestrator-pattern.template` for router/worker structure.

**Best Practice**: <10 tools per worker, narrow context. Each worker loads only relevant context, minimizing token usage and improving accuracy.

**Trade-offs**: Coordination overhead, complex state management. High complexity, high cost.

### Pattern 4: Planning (Plan-and-Execute)

Generates comprehensive multi-step plan before execution begins, separating high-level reasoning from low-level execution.

**Implementation**: Planner analyzes request, outputs structured DAG. Executor iterates through plan, executing steps. Executor can update plan if earlier step reveals new information (replanning).

**When to Use**: Long-horizon tasks, software feature development, complex multi-step workflows.

**Template**: See `templates/planning-pattern.template` for planner/executor structure.

**Best Practice**: Update plan if earlier step reveals new information. Plan should be structured DAG, not linear sequence.

**Trade-offs**: High initial latency. Rigid if plan fails without replanning. High complexity, medium cost.

## Best Practices

### Architecture

- **Clean Architecture Boundaries**: Domain layer independent of frameworks. Use dependency injection.
- **Framework-Agnostic Domain**: Agent reasoning logic testable without real model calls.
- **Progressive Disclosure**: Use MCP for large data sources. Process within secure environment, return insights only.

### Reliability

- **Idempotency Keys**: Mandatory for all state-changing operations. Generate deterministically from function name and parameters.
- **Retry with Jitter**: Exponential backoff with randomness prevents thundering herd. Base delay 1s, max 10s, 3 retries.
- **Circuit Breakers**: Block consistently failing tools. Update system prompt dynamically: "Search Tool is offline. Use alternatives."
- **Guardrails**: Input/output validation. Run in parallel or blocking mode. Pre-canned safety responses for violations.

### Security

- **Zero Trust Identity**: Use SPIFFE/SPIRE for workload identity. Dynamic SVIDs instead of static API keys.
- **Mutual TLS (mTLS)**: SPIRE performs node and workload attestation before issuing SVIDs.
- **Policy Enforcement**: Tools enforce policies based on SPIFFE ID (e.g., "Only finance-analyst SPIFFE ID can execute transfers").

### Testing

- **Contract Testing (Pact)**: Agent defines tool expectations. Tool provider verifies contract in CI pipeline.
- **Architectural Tests**: Use pytest-archon or ArchUnit. Rule: "Domain layer must NOT import from Infrastructure."
- **Evaluations (Evals)**: LLM-as-a-Judge grades execution traces. Criteria: correctness, tool usage efficiency, tone.

### Performance

- **Context Window Management**: Avoid "Lost in the Middle" phenomena. Keep tools <10 per agent.
- **Progressive Disclosure**: MCP servers process large data, return summaries. Reduces token costs and context pollution.

## Workarounds

### Workaround 1: Idempotency Keys

**When**: State-changing operations, retry scenarios, payment APIs, database writes.

**Action**: Generate deterministic key from function name and parameters (hash of sorted JSON). Server-side Redis cache checks key existence. If exists, return cached response. If not, process and cache result with TTL (86400s default).

**Trade-offs**: 
- Maintenance debt: Cache invalidation complexity, TTL management
- Limitations: Requires distributed cache (Redis), storage overhead
- Future considerations: Key collision handling, cache warming strategies

**Template**: See `templates/idempotency-decorator.template` for Python decorator implementation.

### Workaround 2: Exponential Backoff with Jitter

**When**: Rate limits, transient failures, network timeouts, API throttling.

**Action**: Calculate delay: `sleep = min(cap, base * 2^attempt) + random_uniform(0, 0.5 * delay)`. Base delay 1s, max 10s, 3 retries. Jitter desynchronizes multiple agents retrying simultaneously.

**Trade-offs**:
- Maintenance debt: Tuning base delay and max attempts
- Limitations: Latency increase, may not resolve persistent failures
- Future considerations: Adaptive backoff based on error types, circuit breaker integration

**Template**: See `templates/retry-backoff.template` for implementation.

### Workaround 3: Circuit Breaker Pattern

**When**: Consistently failing tools, service outages, cascading failures.

**Action**: State machine: Closed (normal) → Open (blocked after N failures) → Half-Open (probe after timeout). Open state returns immediate error. Half-open allows one probe request. On success, return to Closed.

**Trade-offs**:
- Maintenance debt: Tuning failure threshold, recovery timeout
- Limitations: False positives may block healthy services, recovery detection complexity
- Future considerations: Adaptive thresholds, health check integration

**Template**: See `templates/circuit-breaker.template` for state machine implementation.

### Workaround 4: Guardrails Middleware

**When**: Input/output validation, safety enforcement, PII detection, prompt injection prevention.

**Action**: Pre-execution: Scan user queries for PII, prompt injection ("Ignore previous instructions"), off-topic requests. Post-execution: Scan agent responses for hallucinated URLs, toxic content, sensitive data leakage. Tripwire detection halts request, returns pre-canned safety response.

**Trade-offs**:
- Maintenance debt: False positive handling, rule maintenance
- Limitations: Latency overhead, may block legitimate requests
- Future considerations: ML-based detection, adaptive thresholds

**Template**: See `templates/guardrails-middleware.template` for interception layer.

## Anti-Patterns to Avoid

### Anti-Pattern 1: God Agent (Context Overload)

**Issue**: Single monolithic agent with 50+ tools and massive system prompt. Suffers from "Lost in the Middle" phenomena: as context fills with tool definitions and history, model's ability to attend to specific instructions degrades. Leads to tool confusion (selecting wrong tool) and instruction drift (ignoring safety guardrails).

**Detection**: 
- Single agent with >10 tools
- Tool confusion (wrong tool selected)
- Instruction drift (safety rules ignored)
- Context window consistently full

**Resolution**: Apply Single Responsibility Principle. Decompose into Swarm of specialized agents, each with <10 tools. Use Orchestrator-Workers pattern for routing.

**Example**:
```python
# ❌ Bad: God Agent
agent = Agent(tools=[tool1, tool2, ..., tool50])  # 50+ tools

# ✅ Good: Swarm
orchestrator = RouterAgent()
billing_agent = Agent(tools=[billing_tools])  # <10 tools
support_agent = Agent(tools=[support_tools])  # <10 tools
```

### Anti-Pattern 2: Infinite ReAct Loops (The "Stutter")

**Issue**: Agent enters cycle of repeating same thought and action without making progress. Example: "Thought: Check status. Action: get_status(). Observation: 'Pending'. Thought: Check status. Action: get_status()..." Agent lacks termination condition or sense of "time passing."

**Detection**:
- Duplicate consecutive tool calls
- No termination condition
- Same observation repeated
- Step count exceeds reasonable limit

**Resolution**: 
- Short-term memory: Detect duplicate consecutive tool calls
- Step limit: Enforce hard cap on ReAct steps (max_iterations=15)
- Jitter: If loop detected, inject system prompt: "You are repeating yourself. Try a different strategy"

**Example**:
```python
# ❌ Bad: No loop detection
while True:
    thought, action = agent.react()
    observation = execute(action)
    # Can loop forever

# ✅ Good: Loop detection
seen_actions = set()
for step in range(max_iterations):
    thought, action = agent.react()
    if action in seen_actions:
        agent.inject("You are repeating. Try different strategy.")
        break
    seen_actions.add(action)
    observation = execute(action)
```

### Anti-Pattern 3: Hallucination Cascades

**Issue**: In chain of agents, if Agent A hallucinates a fact, Agent B treats it as ground truth, and Agent C amplifies it. Error propagates downstream, becoming "fact." Unlike deterministic microservices, agent outputs are probabilistic. Downstream agents rarely verify upstream outputs.

**Detection**:
- No verification nodes between agents
- Missing source IDs in agent outputs
- Downstream agents trust upstream without validation
- Errors propagate without correction

**Resolution**: 
- Verification nodes: Insert deterministic "Judge" nodes or "Validator" functions between agents
- Evidence citation: Require Agent A to pass source IDs along with summary. If Agent B cannot verify source ID, reject input

**Example**:
```python
# ❌ Bad: No verification
agent_a_output = agent_a.process(input)
agent_b_output = agent_b.process(agent_a_output)  # Trusts without verification

# ✅ Good: Verification node
agent_a_output = agent_a.process(input)
verified = validator.verify(agent_a_output)  # Verification node
if verified:
    agent_b_output = agent_b.process(agent_a_output)
else:
    agent_b_output = agent_b.process(original_input)  # Fallback
```

### Anti-Pattern 4: Open Loop Execution

**Issue**: Allowing agent to execute state-changing operations (DELETE, Refund, Transfer) without human-in-the-loop (HITL) confirmation. Agents have non-zero error rate. Hallucination in read-only task is annoying; in write task, it is destructive.

**Detection**:
- State-changing operations without approval
- DELETE/Refund/Transfer executed directly
- No HITL middleware
- Sensitive operations in agent tool list

**Resolution**: Implement Human-in-the-Loop middleware. For sensitive tools, agent pauses execution and pushes "Request for Approval" event. Workflow resumes only after human signal is received.

**Example**:
```python
# ❌ Bad: Direct execution
@agent.tool
def delete_user(user_id: str):
    db.delete(user_id)  # Destructive, no approval

# ✅ Good: HITL middleware
@agent.tool
def delete_user(user_id: str):
    approval = hitl.request_approval("delete_user", {"user_id": user_id})
    if approval.granted:
        db.delete(user_id)
    else:
        return {"error": "Operation cancelled"}
```

## Real-World Examples

### Example 1: Security Audit Agent (PydanticAI with Clean Architecture)

Minimal implementation demonstrating Clean Architecture with structured output and dependency injection:

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool
from typing import List

# Domain Layer (Entity)
class SecurityAuditResult(BaseModel):
    vulnerabilities_found: int
    severity_level: str = Field(description="Low, Medium, High, or Critical")
    action_items: List[str]
    requires_human_escalation: bool

# Infrastructure Layer (Dependencies)
class AgentDeps:
    def __init__(self, db_conn_str: str, api_key: str):
        self.db_conn_str = db_conn_str
        self.api_key = api_key

# Use Case Layer (Agent Definition)
security_agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDeps,
    result_type=SecurityAuditResult,  # Enforces structured output
    system_prompt=(
        "You are a Senior Security Auditor. "
        "Analyze logs and report vulnerabilities. "
        "Be conservative: if unsure, mark as High severity."
    )
)

# Interface Adapter (Tool)
@security_agent.tool
async def scan_logs(ctx: RunContext, query: str) -> str:
    """Retrieves logs from SIEM system matching the query."""
    # Uses ctx.deps.db_conn_str for connection
    return "Log Entry: User 'admin' failed login 50 times from IP 192.168.1.5"

# Application Layer (Execution)
async def run_audit_workflow():
    deps = AgentDeps(db_conn_str="postgres://...", api_key="secret")
    result = await security_agent.run("Check for brute force attacks in the last hour.", deps=deps)
    
    if result.data.requires_human_escalation:
        print(f"ALARM: {result.data.severity_level} Threat Detected!")
        print(f"Actions: {result.data.action_items}")
```

### Example 2: Reflection Loop (LangGraph)

Minimal implementation demonstrating Reflection pattern with critique step and termination guard:

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[str]
    draft: str
    critique: str
    revision_count: int

def generator_node(state: AgentState):
    """Generates initial draft or revises based on critique."""
    revision = state.get("revision_count", 0)
    draft = f"Draft content (Revision {revision})"
    return {"draft": draft, "revision_count": revision + 1}

def reflection_node(state: AgentState):
    """Critiques the draft acting as 'Teacher'."""
    draft = state["draft"]
    if "bad" in draft or state["revision_count"] < 2:
        critique = "Draft is too short. Expand it."
    else:
        critique = "Looks good."
    return {"critique": critique}

def should_continue(state: AgentState):
    # Guardrail: Prevent infinite loops
    if state["revision_count"] > 3:
        return END
    # Acceptance criteria
    if state["critique"] == "Looks good.":
        return END
    return "generator"

workflow = StateGraph(AgentState)
workflow.add_node("generator", generator_node)
workflow.add_node("reflector", reflection_node)
workflow.set_entry_point("generator")
workflow.add_edge("generator", "reflector")
workflow.add_conditional_edges("reflector", should_continue)
app = workflow.compile()
```

## Related Skills

- `implementing-resilient-agentic-architecture`: For distributed systems patterns (shuffle sharding, cell-based architecture, static stability)
- `implementing-infraops-agent`: For infrastructure orchestration and platform engineering

## Notes

- Replace framework-specific code with framework-agnostic patterns when possible
- Always implement reliability primitives (idempotency, retry, circuit breakers) for production use
- Use Clean Architecture to enable testing without real LLM calls
- Progressive disclosure via MCP reduces token costs and context pollution
- Structure for Interleaved Guidance: Sections (Common Patterns, Best Practices, Workarounds, Anti-Patterns) are clearly marked for Phase 6 workflow extraction
- Section Naming: Use exact section names ("Common Patterns", "Best Practices", "Workarounds", "Anti-Patterns to Avoid") to support automatic extraction

