---
name: evaluating-code-quality
description: Performs comprehensive code quality analysis using Evaluator-Optimizer pattern. Provides iterative feedback for code improvements. Use when reviewing code quality, security, architectural consistency, or when the user mentions code review, quality check, or evaluation.
---

# Evaluating Code Quality

This skill guides comprehensive code quality analysis using the Evaluator-Optimizer pattern for iterative improvement.

## Evaluator-Optimizer Pattern

This pattern implements a recursive feedback loop:
1. Generate evaluation of code quality
2. Identify areas for improvement
3. Provide specific, actionable feedback
4. Allow executor to fix issues
5. Re-evaluate until quality standards are met

## Review Process

1. **Read and Analyze**: Examine code files using Read and Grep
2. **Check Standards**: Verify code follows project conventions (see [src/CLAUDE.md](../../../src/CLAUDE.md))
3. **Identify Issues**: Find bugs, anti-patterns, and quality issues
4. **Rate Severity**: Categorize issues as CRITICAL, HIGH, MEDIUM, LOW
5. **Provide Feedback**: Give specific, actionable recommendations with code examples
6. **Verify Fixes**: Re-review after fixes are applied

## Quality Criteria

Reference quality metrics in [quality-metrics.md](quality-metrics.md) (one level deep).

### Code Style
- Follows PEP 8 and project conventions
- Consistent formatting and naming
- Proper indentation and spacing

### Type Safety
- Proper type hints throughout
- No `Any` types without justification
- Type-safe function signatures

### Error Handling
- Appropriate exception handling
- Meaningful error messages
- Proper error propagation

### Documentation
- Clear docstrings (Google style)
- Inline comments for complex logic
- README updates when needed

### Testing
- Adequate test coverage (>80%)
- Tests for success and failure paths
- Integration tests for critical paths

### Performance
- Efficient algorithms and data structures
- No obvious performance bottlenecks
- Proper resource management

### Security
- No obvious security vulnerabilities
- Input validation
- Secure authentication/authorization

### Maintainability
- Clean, readable code
- Well-organized structure
- DRY principles followed

## Feedback Format

Provide feedback in this format:

```markdown
## Issue: [Title]
**Severity**: [CRITICAL|HIGH|MEDIUM|LOW]
**Location**: [file:line]
**Description**: [What's wrong]
**Recommendation**: [How to fix]
**Example Fix**:
```python
# Before
[bad code]

# After
[good code]
```
```

## Examples

**Example 1: Type Safety Issue**
- Issue: Missing type hints
- Severity: MEDIUM
- Recommendation: Add type hints to function signature
- Example fix provided

**Example 2: Security Vulnerability**
- Issue: SQL injection risk
- Severity: CRITICAL
- Recommendation: Use parameterized queries
- Example fix provided

