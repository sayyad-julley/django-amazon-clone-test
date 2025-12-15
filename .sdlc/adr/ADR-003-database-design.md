# ADR-003: Database Design and Entity Relationships

## Status
Accepted

## Date
2024-12-10

## Context
The e-commerce platform requires a database schema that supports:
- Hierarchical product categories
- Flexible product attributes (variants, details, media)
- Order management with delivery tracking
- Inventory management with transaction logging

## Decision
We will use a **relational database (SQLite/PostgreSQL)** with the following key design patterns:

### 1. Category Hierarchy
Two-level hierarchy using ForeignKey relationship:
```
Categories -> SubCategories -> Products
```

### 2. Product Extensions (EAV Pattern)
Entity-Attribute-Value pattern for flexible product attributes:
- `ProductDetails`: Key-value pairs for specifications
- `ProductAbout`: Bullet points/features
- `ProductTags`: Searchable tags
- `ProductMedia`: Multiple images/videos per product

### 3. Product Variants
EAV-style variant system:
```
ProductVarient (e.g., "Color", "Size")
  -> ProductVarientItems (e.g., "Red", "Large") -> Products
```

### 4. Inventory Event Sourcing
Transaction log pattern for inventory:
```python
class ProductTransaction(models.Model):
    transaction_type_choices = ((1,"BUY"),(2,"SELL"))
    product_id = ForeignKey(Products)
    transaction_product_count = IntegerField()
    transaction_type = CharField(choices=transaction_type_choices)
    transaction_description = CharField()
    created_at = DateTimeField(auto_now_add=True)
```

### 5. Order Status Tracking
Separate status table for order lifecycle:
```
CustomerOrders -> OrderDeliveryStatus (multiple status entries)
```

## Entity Relationship Summary
- **20+ entities** with clear domain boundaries
- **User Hierarchy**: CustomUser -> Profile Models
- **Product Hierarchy**: Categories -> SubCategories -> Products
- **Product Extensions**: Products -> Media/Details/Tags/Variants
- **Commerce Flow**: Products -> Orders -> Delivery Status
- **Audit Trail**: Products -> ProductTransaction

## Consequences

### Positive
- Flexible product attributes without schema changes
- Full inventory audit trail
- Order status history preserved
- Clean separation of concerns

### Negative
- Price fields as CharField (should be DecimalField)
- Missing customer_id in CustomerOrders
- is_active as IntegerField (should be BooleanField)
- Inconsistent naming conventions

### Required Migrations
1. Convert price fields to DecimalField
2. Add customer_id ForeignKey to CustomerOrders
3. Convert is_active fields to BooleanField
4. Standardize naming conventions

## Data Integrity Considerations
- Use database transactions for order creation
- Implement database-level constraints where possible
- Add indexes on frequently queried fields (url_slug, is_active)
- Consider partitioning for ProductTransaction growth

## Related Decisions
- ADR-001: Monolithic Django Architecture
- ADR-002: Multi-Role Authentication
