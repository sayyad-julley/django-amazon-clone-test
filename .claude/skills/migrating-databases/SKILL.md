---
name: migrating-databases
description: Executes database migrations with validation and rollback support. Use when migrating database schemas, creating migration scripts, or when the user mentions database changes, migrations, or schema updates.
---

# Migrating Databases

This skill guides database migration execution with validation and rollback support.

## Migration Process

Copy this checklist and track your progress:

Migration Progress:
- [ ] Analyze current schema
- [ ] Create migration script
- [ ] Validate migration syntax
- [ ] Test migration on development database
- [ ] Create rollback script
- [ ] Document migration changes
- [ ] Execute migration on target database
- [ ] Verify migration success

## Migration Script Creation

### SQL Migrations
1. Create migration file with timestamp
2. Write UP migration (forward changes)
3. Write DOWN migration (rollback changes)
4. Validate SQL syntax
5. Test on development database

### ORM Migrations (Django, SQLAlchemy, etc.)
1. Generate migration using framework tools
2. Review generated migration
3. Customize if needed
4. Test migration
5. Create rollback plan

## Validation Steps

Run validation scripts (see [validation/](validation/) for scripts):

1. **Syntax Check**: Validate SQL/ORM syntax
2. **Dependency Check**: Verify all dependencies exist
3. **Data Integrity**: Check for data loss risks
4. **Performance**: Estimate migration duration
5. **Rollback Test**: Verify rollback works

## Rollback Support

Always create rollback scripts:

```sql
-- UP Migration
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- DOWN Migration (Rollback)
ALTER TABLE users DROP COLUMN email;
```

## Safety Checks

Before executing migration:
- [ ] Backup database
- [ ] Test on development environment
- [ ] Verify rollback script works
- [ ] Check for data loss risks
- [ ] Estimate downtime
- [ ] Plan maintenance window

## Examples

**Example 1: Adding Column**
- Migration: `ALTER TABLE users ADD COLUMN email VARCHAR(255)`
- Rollback: `ALTER TABLE users DROP COLUMN email`
- Validation: Check column doesn't exist before adding

**Example 2: Creating Table**
- Migration: `CREATE TABLE orders (...)`
- Rollback: `DROP TABLE orders`
- Validation: Check table doesn't exist before creating

## Execution Commands

Reference exact commands in [commands.md](commands.md) (one level deep).

Run migrations with explicit execution intent:
- "Run migration script: `python manage.py migrate`"
- "Execute rollback: `python manage.py migrate app_name migration_number`"

