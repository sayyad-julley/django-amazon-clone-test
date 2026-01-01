---
name: coderabbit-severity-filter
description: Filter CodeRabbit review results by severity to distinguish actionable failures from silent warnings
version: 1.0.0
---

# CodeRabbit Severity Filter Skill

This skill filters CodeRabbit review results by severity, allowing the orchestration to distinguish between actionable failures (CRITICAL/MAJOR) and silent warnings (MINOR/INFO).

## Purpose

The skill acts as a decision layer between the `wait_for_coderabbit_review` tool and the main agent, providing intelligent filtering and state management. It ensures that only critical issues that require fixes are surfaced to the agent, while style nits and non-actionable warnings are silently ignored.

## Severity Levels

The skill recognizes four severity levels:

- **CRITICAL**: Issues that break functionality or security (e.g., SQL injection, infinite loops, memory leaks)
- **MAJOR**: Significant bugs that affect functionality (e.g., logic errors, null pointer exceptions)
- **WARNING**: Style issues, formatting problems, or minor suggestions (e.g., missing trailing commas, line length violations)
- **INFO**: Nitpicks, documentation issues, or non-breaking refactor suggestions (e.g., missing docstrings, variable renaming suggestions)

## Default Threshold

The default threshold is **MAJOR**, meaning only CRITICAL and MAJOR issues trigger action. WARNING and INFO issues are automatically ignored.

## Decision Logic

- **Actionable Failures** (CRITICAL/MAJOR): Trigger `PLANNING` state - agent receives filtered findings and must fix issues
- **Silent Warnings** (WARNING/INFO): Trigger `COMPLETE` state - issues are logged but hidden from agent

## Ignore Criteria

The following categories are automatically classified as WARNING/INFO and ignored:

1. **Style & Formatting**: Missing trailing commas, indentation errors, line-length violations, whitespace inconsistencies
2. **Documentation**: Missing docstrings, typos in comments, outdated TODOs, missing type hints (unless explicitly required)
3. **Non-Breaking Refactors**: Suggestions to use list comprehension, renaming local variables, code style improvements
4. **Missing Tests for Edge Cases**: Missing tests for rare edge cases (< 1% probability), unless the module is mission-critical

## Usage in Orchestration

The skill is automatically invoked after the `wait_for_coderabbit_review` tool returns results. The orchestration flow:

1. CodeRabbit review tool returns raw review content
2. SeverityFilterSkill evaluates and filters findings
3. If action required: Agent receives filtered findings and loops back to PLANNING
4. If no action required: Workflow completes with warnings/info logged but hidden

## Configuration

The skill can be configured via environment variable:

- `CODERABBIT_SEVERITY_THRESHOLD`: Default "MAJOR", options: "INFO", "WARNING", "MAJOR", "CRITICAL"

