---
name: executing-file-modifications
description: Executes granular file modifications following project conventions. Handles boilerplate generation, unit testing, and CSS styling. Use when implementing specific code changes, generating standard code patterns, or when the user mentions file editing or code generation.
---

# Executing File Modifications

This skill guides the execution of granular file modifications following project conventions.

## Implementation Process

1. **Understand Requirements**: Review what needs to be implemented
2. **Examine Existing Patterns**: Use Read to see how similar code is structured
3. **Follow Conventions**: Adhere to project standards (see [src/CLAUDE.md](../../../src/CLAUDE.md))
4. **Implement Changes**: Create or modify files as needed
5. **Add Tests**: Write unit tests for new functionality
6. **Verify**: Run tests and linting

## Code Generation Patterns

### Python Files
- Use type hints for all functions
- Follow PEP 8 style guide
- Add Google-style docstrings
- Handle errors with try/except

### Test Files
- Use pytest fixtures for setup
- Follow AAA pattern (Arrange-Act-Assert)
- Test both success and failure paths
- Use descriptive test names

### Configuration Files
- Follow existing format (YAML, JSON, etc.)
- Validate structure before writing
- Include comments for clarity

## Boilerplate Templates

Reference project-specific templates in [templates/](templates/) (one level deep).

### Service Class Template
```python
from typing import Optional, List

class ServiceName:
    """Service description."""
    
    def __init__(self, dependency: DependencyType):
        """Initialize service."""
        self._dependency = dependency
    
    async def method_name(self, param: str) -> Optional[ResultType]:
        """Method description.
        
        Args:
            param: Parameter description
        
        Returns:
            Result description
        """
        # Implementation
        pass
```

### Test Class Template
```python
import pytest
from service import ServiceName

class TestServiceName:
    """Test suite for ServiceName."""
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return ServiceName(mock_dependency)
    
    def test_method_success(self, service):
        """Test successful method execution."""
        result = service.method_name("test")
        assert result is not None
```

## Validation Scripts

Run validation scripts after modifications:
- `pytest` - Run tests
- `flake8 src/` - Check style
- `mypy src/` - Check types

Reference validation scripts in [scripts/](scripts/) (one level deep).

## Best Practices

- **Read before writing**: Examine similar files first
- **Follow patterns**: Use existing code as templates
- **Test immediately**: Write tests as you code
- **Verify changes**: Run validation before completing

