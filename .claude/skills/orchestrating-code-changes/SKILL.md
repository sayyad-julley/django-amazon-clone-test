---
name: orchestrating-code-changes
description: Breaks down complex coding tasks into subtasks, delegates to executors, and synthesizes results. Use when managing multi-file code changes, coordinating complex refactoring tasks, or when the user mentions orchestration, task decomposition, or multi-file modifications.
---

# Orchestrating Code Changes

This skill guides the orchestration of complex coding tasks by breaking them into manageable subtasks and delegating to appropriate subagents.

## Task Decomposition

Break complex tasks into manageable subtasks:

1. **Analyze requirements** - Understand what needs to be done
2. **Identify dependencies** - Determine task order
3. **Create subtasks** - Break into atomic units

## Delegation Pattern

Delegate to subagents using Task tool:

**For implementation tasks**: Delegate to executor subagent
- Example: "Use the executor agent to implement the authentication module"

**For quality review**: Delegate to evaluator subagent
- Example: "Use the evaluator agent to review code quality"

**For security audit**: Delegate to security-reviewer subagent
- Example: "Use the security-reviewer agent to audit for vulnerabilities"

## Workflow Checklist

Copy this checklist and track your progress:

Task Progress:
- [ ] Analyze requirements
- [ ] Decompose into subtasks
- [ ] Delegate to appropriate subagents
- [ ] Synthesize results
- [ ] Verify completion

## Task Breakdown Patterns

### Multi-File Changes
1. Identify all files that need modification
2. Determine modification order (dependencies first)
3. Delegate file modifications to executor
4. Verify all changes are consistent

### Refactoring Tasks
1. Analyze current code structure
2. Identify refactoring targets
3. Plan refactoring steps to maintain functionality
4. Delegate implementation to executor
5. Request evaluator review after changes

### Feature Implementation
1. Break feature into components
2. Identify new files to create
3. Identify existing files to modify
4. Delegate component implementation to executor
5. Request evaluator review for each component
6. Synthesize components into complete feature

## Examples

**Example 1: Adding Authentication**
- Subtask 1: Create authentication service (delegate to executor)
- Subtask 2: Create authentication controller (delegate to executor)
- Subtask 3: Review code quality (delegate to evaluator)
- Subtask 4: Security audit (delegate to security-reviewer)
- Synthesize: Combine all components

**Example 2: Database Migration**
- Subtask 1: Create migration script (delegate to executor)
- Subtask 2: Update models (delegate to executor)
- Subtask 3: Review migration safety (delegate to evaluator)
- Synthesize: Verify migration is ready

