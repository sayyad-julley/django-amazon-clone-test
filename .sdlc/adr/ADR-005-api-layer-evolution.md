# ADR-005: REST API Layer Evolution

## Status
Proposed

## Date
2024-12-10

## Context
The current Django e-commerce platform uses server-side rendered templates. To support:
- Mobile applications
- Third-party integrations
- Frontend SPA migration (React/Vue)

We need to add a REST API layer.

## Decision
We will implement a **Django REST Framework (DRF)** API layer alongside the existing template-based views.

### Phased Implementation

#### Phase 1: Read-Only APIs (Foundation)
```
GET  /api/v1/categories/
GET  /api/v1/categories/{id}/
GET  /api/v1/products/
GET  /api/v1/products/{id}/
GET  /api/v1/products/{id}/media/
GET  /api/v1/products/{id}/reviews/
```

#### Phase 2: Authentication APIs
```
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/logout/
POST /api/v1/auth/refresh/
GET  /api/v1/auth/profile/
PUT  /api/v1/auth/profile/
```

#### Phase 3: Customer Operations
```
GET    /api/v1/cart/
POST   /api/v1/cart/items/
DELETE /api/v1/cart/items/{id}/
POST   /api/v1/orders/
GET    /api/v1/orders/
GET    /api/v1/orders/{id}/
POST   /api/v1/reviews/
```

#### Phase 4: Merchant APIs
```
GET    /api/v1/merchant/products/
POST   /api/v1/merchant/products/
PUT    /api/v1/merchant/products/{id}/
GET    /api/v1/merchant/inventory/
POST   /api/v1/merchant/inventory/stock/
GET    /api/v1/merchant/orders/
```

### Technical Approach

#### Authentication
- JWT tokens via `djangorestframework-simplejwt`
- Token refresh mechanism
- Optional session auth for admin operations

#### Serializers
```python
class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(source='subcategories_id')
    merchant = MerchantSerializer(source='added_by_merchant')
    media = ProductMediaSerializer(many=True, source='productmedia_set')

    class Meta:
        model = Products
        fields = ['id', 'product_name', 'brand', 'product_max_price',
                  'product_discount_price', 'subcategory', 'merchant', 'media']
```

#### Versioning
- URL-based versioning: `/api/v1/`, `/api/v2/`
- Support for backward compatibility

#### Pagination
- Cursor-based pagination for product lists
- Page-based pagination for admin views

## Alternatives Considered

### GraphQL
- **Pros**: Flexible queries, single endpoint
- **Cons**: Learning curve, caching complexity, over-fetching protection needed

### gRPC
- **Pros**: High performance, strong typing
- **Cons**: Not suitable for web clients, additional infrastructure

## Consequences

### Positive
- Enable mobile app development
- Support SPA frontend migration
- Third-party integration capability
- Decoupled frontend/backend development

### Negative
- Additional maintenance surface
- Need for API documentation
- Authentication complexity (two auth systems)

### Required Work
1. Install DRF and JWT packages
2. Create serializers for all models
3. Implement ViewSets with permissions
4. Add OpenAPI/Swagger documentation
5. Set up API rate limiting

## Related Decisions
- ADR-001: Monolithic Architecture
- ADR-004: Security Improvements
