---
name: implementing-high-performance-fastapi-production
description: Implements high-performance FastAPI systems by applying domain-driven architecture, asynchronous mastery, and production hardening patterns. Use when building scalable Python backends, integrating with HIMS Platform stacks, or optimizing for high-concurrency environments.
version: 1.0.0
dependencies:
  - python>=3.10
  - fastapi>=0.127.0
  - pydantic>=2.0.0
  - sqlmodel>=0.0.8
  - uvicorn>=0.22.0
  - gunicorn>=21.2.0
  - sqlalchemy>=2.0.0
---

# Implementing High-Performance FastAPI Production

## Overview

This skill provides the architectural blueprints and operational standards for engineering professional-grade FastAPI systems. It focuses on maximizing throughput using the ASGI event loop, ensuring type safety with Pydantic V2/SQLModel, and hardening the service layer for production environments like the HIMS Platform.

## When to Use

Use this skill when:
- Designing a new FastAPI microservice from scratch.
- Refactoring a "god file" FastAPI app into a scalable domain-based architecture.
- Optimizing an existing service for high-concurrency AI/ML inference or healthcare data transformation.
- Integrating FastAPI with enterprise identity providers (Scalekit) or authorization engines (Permit.io).

## Prerequisites

- Python 3.10+ (for modern type hint features).
- Understanding of `async/await` syntax.
- Redis (if using ARQ for background tasks) or PostgreSQL (for SQLModel).

## Execution Steps

### Step 1: Initialize Domain-Based Structure

Copy this checklist to track your implementation progress:

```markdown
FastAPI Production Readiness:
- [ ] 1. Initialize `src/` directory with domain sub-packages
- [ ] 2. Configure Pydantic Settings in `config.py`
- [ ] 3. Set up Async Database Session (SQLModel + asyncpg)
- [ ] 4. Implement Multi-Model Inheritance for core resources
- [ ] 5. Apply Security Headers and Rate Limiting middleware
- [ ] 6. Instrument with OpenTelemetry for observability
```

### Step 2: Implement Core Architecture

1.  **Define Models**: Use SQLModel. See [templates/TEMPLATES.md](templates/TEMPLATES.md) for hierarchy.
2.  **Create Service Layer**: Extract business logic from routers into `service.py`.
3.  **Setup Dependencies**: Use `Depends` for DI chains. See [templates/TEMPLATES.md](templates/TEMPLATES.md) for DB session setup.

## Technical Reference

For detailed information on server gateways, execution mechanics, and enterprise integrations, see the [resources/REFERENCE.md](resources/REFERENCE.md).

## Code Templates

For reusable implementations of database sessions, models, and security middleware, see [templates/TEMPLATES.md](templates/TEMPLATES.md).

## Common Patterns

### 1. Module-Functionality (Domain) Pattern
Avoid "god files" by grouping routes, models, and logic by business domain.

```text
src/
├── clinical/              # Clinical domain
│   ├── router.py          # Routes
│   ├── schemas.py         # Pydantic models (FHIR-compliant)
│   ├── service.py         # Business logic
│   └── dependencies.py    # Local auth/RBAC checks
```

### 2. Multi-Model Inheritance
Separate internal DB state from public API contracts to prevent sensitive data leakage. See [templates/TEMPLATES.md](templates/TEMPLATES.md) for the code pattern.

### 3. Service Layer Decoupling
Keep routes thin; delegate complex I/O and logic to services.

```python
# router.py
@router.post("/", response_model=ProjectPublic)
async def create_project(data: ProjectCreate, service: ProjectService = Depends()):
    return await service.create_user_project(data)
```

## Workarounds

| Challenge | Workaround | Implementation |
| :--- | :--- | :--- |
| **Circular Dependencies** | String Forward Refs | Use `doctor: 'Doctor'` in type hints. |
| **Ref Reference Error** | `model_rebuild()` | Call `User.model_rebuild()` after all modules load. |
| **Blocking Code in Async** | `run_in_threadpool` | Offload blocking calls: `await run_in_threadpool(sync_func)`. |

## Anti-Patterns to Avoid

- **Blocking the Event Loop**: Never use `time.sleep()` or `requests` inside `async def`. Use `anyio.sleep()` or `httpx`.
- **Shared Migrations**: Don't let Alembic and Flyway manage the same tables. Designate a primary owner (usually Flyway for shared DBs).
- **Single Model Trap**: Using the same Pydantic model for input, output, and DB storage leads to security vulnerabilities.
- **Global Auth State**: Avoid global variables for user context; use FastAPI Dependency Injection for thread-safe session management.

## Security & Hardening

1.  **Production Gateways**: Always run Gunicorn with `UvicornWorker`. See [resources/REFERENCE.md](resources/REFERENCE.md).
2.  **Hardened Headers**: Implement HSTS, X-Frame-Options, and CSP via middleware.
3.  **HIMS Stack Integration**: Detailed guidance for Scalekit and Permit.io is in [resources/REFERENCE.md](resources/REFERENCE.md).
