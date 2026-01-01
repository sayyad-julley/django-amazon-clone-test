---
name: triaging-performance-regressions
description: Identifies and analyzes performance regressions using profiling and metrics analysis. Use when investigating performance issues, latency spikes, or when the user mentions performance problems, slow queries, or bottlenecks.
---

# Triaging Performance Regressions

This skill guides the identification and analysis of performance regressions using profiling and metrics.

## Regression Analysis Process

Copy this checklist and track your progress:

Analysis Progress:
- [ ] Identify performance issue
- [ ] Collect baseline metrics
- [ ] Profile affected components
- [ ] Identify root cause
- [ ] Propose solution
- [ ] Verify fix

## Decision Points

Determine the type of regression:

**Type A: Database Query Regression** → Follow "Database Analysis" workflow below
**Type B: API Latency Regression** → Follow "API Analysis" workflow below
**Type C: Memory/Resource Regression** → Follow "Resource Analysis" workflow below

## Database Analysis Workflow

1. **Identify Slow Queries**
   - Check query logs
   - Use EXPLAIN ANALYZE
   - Identify missing indexes

2. **Analyze Query Patterns**
   - Check for N+1 queries
   - Verify join efficiency
   - Review query plans

3. **Optimize**
   - Add missing indexes
   - Refactor queries
   - Add query caching

## API Analysis Workflow

1. **Profile Endpoints**
   - Measure response times
   - Identify slow endpoints
   - Check request/response sizes

2. **Analyze Dependencies**
   - Check external API calls
   - Review database queries
   - Verify caching effectiveness

3. **Optimize**
   - Add caching layers
   - Optimize database queries
   - Reduce payload sizes

## Resource Analysis Workflow

1. **Monitor Resources**
   - Check CPU usage
   - Monitor memory consumption
   - Review disk I/O

2. **Identify Bottlenecks**
   - Find memory leaks
   - Identify CPU-intensive operations
   - Check I/O bottlenecks

3. **Optimize**
   - Fix memory leaks
   - Optimize algorithms
   - Improve I/O operations

## Profiling Tools

Reference performance analysis scripts in [scripts/](scripts/) (one level deep).

### Python Profiling
```bash
# CPU profiling
python -m cProfile -o profile.stats script.py

# Memory profiling
python -m memory_profiler script.py
```

### Database Profiling
```sql
-- Enable query logging
SET log_min_duration_statement = 1000;

-- Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM table;
```

## Metrics Collection

Collect these metrics:
- Response time (p50, p95, p99)
- Throughput (requests per second)
- Error rate
- Resource utilization (CPU, memory, disk)

## Root Cause Analysis

1. **Compare Metrics**: Baseline vs current
2. **Identify Changes**: Code changes, deployments, traffic
3. **Correlate Events**: Link regressions to changes
4. **Verify Hypothesis**: Test assumptions

## Examples

**Example 1: Slow API Endpoint**
- Issue: `/api/users` response time increased 3x
- Analysis: N+1 query problem identified
- Solution: Add eager loading, reduce queries
- Verification: Response time back to baseline

**Example 2: Database Query Regression**
- Issue: User lookup query slow after schema change
- Analysis: Missing index on new column
- Solution: Add index on frequently queried column
- Verification: Query time improved 10x

