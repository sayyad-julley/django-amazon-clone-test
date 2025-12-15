# ADR-004: Security Improvements Roadmap

## Status
Proposed

## Date
2024-12-10

## Context
Security audit of the Django e-commerce platform identified several vulnerabilities that need to be addressed before production deployment.

## Current Security Issues

### Critical (P0)
1. **Hardcoded SECRET_KEY**
   - Location: `DjangoEcommerce/settings.py`
   - Risk: Session hijacking, CSRF bypass

2. **DEBUG=True in production**
   - Location: `DjangoEcommerce/settings.py`
   - Risk: Information disclosure

3. **CSRF Exempt on File Upload**
   - Location: `AdminViews.py:file_upload()`
   - Risk: Cross-site request forgery attacks

### High (P1)
4. **No Role-Based Access Control on Views**
   - Many admin views lack @login_required decorator
   - No permission checking for user_type

5. **Unrestricted File Uploads**
   - No file type validation
   - No file size limits
   - Potential for malicious file uploads

### Medium (P2)
6. **Password Storage**
   - Using set_password() correctly, but no password strength validation

7. **SQL Injection Prevention**
   - Django ORM provides protection, but raw queries should be audited

## Decision
Implement a phased security improvement plan:

### Phase 1: Critical Fixes (Week 1)
```python
# settings.py changes
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

### Phase 2: CSRF & Access Control (Week 2)
```python
# Remove @csrf_exempt, use proper AJAX CSRF handling
# In JavaScript:
# headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}

# Add permission mixin
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type in [1, 2]  # Admin or Staff
```

### Phase 3: File Upload Security (Week 3)
```python
# Add validators
from django.core.validators import FileExtensionValidator
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file_upload(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("File too large")
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Invalid file type")
```

## Consequences

### Positive
- Secure configuration for production
- Protection against common web vulnerabilities
- Role-based access control
- Audit trail for sensitive operations

### Negative
- Additional development effort
- Need for environment configuration
- Potential breaking changes to existing workflows

### Monitoring Required
- Implement security logging
- Monitor failed login attempts
- Track file upload patterns

## Related Decisions
- ADR-001: Monolithic Architecture (security boundary)
- ADR-002: Multi-Role Authentication (access control)
