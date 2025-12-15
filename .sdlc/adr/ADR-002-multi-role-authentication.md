# ADR-002: Multi-Role Authentication Strategy

## Status
Accepted

## Date
2024-12-10

## Context
The e-commerce platform requires four distinct user roles with different permissions:
1. **Admin**: Full system access
2. **Staff**: Limited administrative functions
3. **Merchant**: Product and inventory management
4. **Customer**: Shopping and order functions

We needed to decide how to implement this multi-role system.

## Decision
We will use **Single Table Inheritance (STI)** pattern with Django's AbstractUser and OneToOne profile models.

### Implementation
```python
class CustomUser(AbstractUser):
    user_type_choices = ((1,"Admin"),(2,"Staff"),(3,"Merchant"),(4,"Customer"))
    user_type = models.CharField(max_length=255, choices=user_type_choices)

class AdminUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")

class MerchantUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    gst_details = models.CharField(max_length=255)
    # ... additional merchant-specific fields
```

### Automatic Profile Creation via Signals
```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)
        # ... etc
```

## Alternatives Considered

### Option A: Django Groups & Permissions
- **Pros**: Built-in Django feature
- **Cons**: Less flexible for role-specific data, no profile extension

### Option B: Abstract Base Model with Separate User Tables
- **Pros**: Clean separation, specialized fields per user type
- **Cons**: Complex authentication, harder to switch user types

### Option C: Third-party packages (django-role-permissions)
- **Pros**: Pre-built role management
- **Cons**: Additional dependency, potential upgrade issues

## Consequences

### Positive
- Single authentication backend
- Easy user type checking via `user.user_type`
- Role-specific data stored in profile models
- Automatic profile creation via signals

### Negative
- Manual permission checking required in views
- user_type stored as CharField (should be IntegerField)
- No built-in permission matrix

### Required Improvements
1. Add permission mixins for class-based views
2. Create decorators for role-based access control
3. Consider migrating user_type to IntegerField

## Related Decisions
- ADR-001: Monolithic Django Architecture
- ADR-003: Database Design
