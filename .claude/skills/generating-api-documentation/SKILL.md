---
name: generating-api-documentation
description: Generates API documentation in OpenAPI format with examples and schemas. Use when creating API docs, OpenAPI specifications, or when the user mentions API documentation, Swagger, or OpenAPI.
---

# Generating API Documentation

This skill guides API documentation generation in OpenAPI format with examples and schemas.

## Documentation Process

1. **Analyze API Endpoints**: Identify all endpoints to document
2. **Extract Schemas**: Document request/response schemas
3. **Add Examples**: Provide example requests and responses
4. **Generate OpenAPI Spec**: Create OpenAPI 3.0 specification
5. **Validate**: Verify OpenAPI spec is valid

## OpenAPI Structure

Reference OpenAPI templates in [templates/](templates/) (one level deep).

### Basic Structure
```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
paths:
  /endpoint:
    get:
      summary: Endpoint description
      responses:
        '200':
          description: Success response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseModel'
```

## Schema Documentation

Document all request and response schemas:

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
      required:
        - id
        - name
        - email
```

## Examples Pattern

Show input code → output OpenAPI spec:

**Input**: Python FastAPI endpoint
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "John"}
```

**Output**: OpenAPI spec
```yaml
paths:
  /users/{user_id}:
    get:
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
```

## Helper Assets

Reference OpenAPI templates and examples in [templates/](templates/) (one level deep).

### Common Patterns
- Authentication endpoints
- CRUD operations
- Pagination
- Error responses
- File uploads

## Validation

Validate OpenAPI spec:
- Check syntax with OpenAPI validator
- Verify all endpoints are documented
- Ensure examples match schemas
- Test with Swagger UI

