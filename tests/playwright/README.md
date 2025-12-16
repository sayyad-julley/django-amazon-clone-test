# Playwright-Kualitee Integration

## Overview

This directory contains Playwright tests integrated with Kualitee Test Management using the **Push Model** approach. Tests automatically report their results to Kualitee in real-time.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Playwright    │───▶│   conftest.py    │───▶│   Kualitee API  │
│     Tests       │    │   Hook System    │    │   /execute      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Test Case Mapping

Each test must be mapped to a Kualitee test case using the `@pytest.mark.kualitee_id` marker:

```python
@pytest.mark.kualitee_id("1124940")
def test_login_success(page: Page):
    # Test implementation
    pass
```

## Running Tests

### Prerequisites

1. **Install dependencies:**
   ```bash
   pip install pytest-playwright
   playwright install chromium
   ```

2. **Set environment variables:**
   ```bash
   export KUALITEE_API_TOKEN="your-token-here"
   export LANGSMITH_API_KEY="your-langsmith-key"  # For tracing
   ```

### Execute Tests

```bash
# Run all Playwright tests
pytest tests/playwright/ -v

# Run specific test file
pytest tests/playwright/test_django_auth.py -v

# Run tests with specific marker
pytest tests/playwright/ -m "kualitee_id" -v

# Run in headful mode (visible browser)
pytest tests/playwright/ --headed
```

## Integration Features

### ✅ Automatic Result Reporting
- Tests automatically report Pass/Fail status to Kualitee
- No manual intervention required
- Real-time updates during test execution

### ✅ Error Context
- Failed tests include error messages and stack traces
- Test execution details captured as evidence

### ✅ Project Mapping
- Configured for Django Amazon Clone project (ID: 20317)
- Maps to correct Kualitee workspace automatically

## Test Examples

### Authentication Tests
- `test_login_success` → Kualitee ID: 1124940
- `test_login_invalid_credentials` → Kualitee ID: 1124941
- `test_logout_functionality` → Kualitee ID: 1124942

### Rate Limiting Tests (AGENTIC-116)
- `test_api_rate_limit_enforcement` → Kualitee ID: 1124945
- `test_rate_limit_retry_after_header` → Kualitee ID: 1124946

## Configuration Files

- **conftest.py** - Pytest hooks and Kualitee integration logic
- **pytest.ini** - Test configuration and markers
- **test_django_auth.py** - Example test implementations

## Troubleshooting

### Common Issues

1. **Kualitee API Token Error**
   ```bash
   export KUALITEE_API_TOKEN="dc18debdc8a7d4cf9438a0f2efd552fb"
   ```

2. **Browser Installation**
   ```bash
   playwright install chromium
   ```

3. **Django Server Not Running**
   ```bash
   # Start Django server on localhost:8000
   python manage.py runserver
   ```

### Debugging

```bash
# Run with verbose output
pytest tests/playwright/ -v -s

# Run single test with debug
pytest tests/playwright/test_django_auth.py::test_login_success -v -s

# Check Kualitee integration logs
pytest tests/playwright/ -v | grep "Kualitee"
```

## Best Practices

1. **Test Case IDs**: Always use valid Kualitee test case IDs
2. **Descriptive Names**: Test names should match Kualitee test case titles
3. **Error Handling**: Tests should handle network failures gracefully
4. **Independence**: Each test should be independent and cleanup after itself

## Next Steps

1. **Batch Upload Integration**: Implement JUnit XML report upload for large suites
2. **Auto-Provisioning**: Enable automatic test case creation from test code
3. **CI/CD Integration**: Add to Jenkins/GitHub Actions pipelines
4. **Enhanced Reporting**: Add screenshots and detailed evidence collection