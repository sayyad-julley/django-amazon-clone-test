---
dependencies:
- org.junit:junit-bom:6.0.1
- java>=21
description: Implements JUnit 6.0.1 tests in Java 21 by applying patterns (Virtual
  Thread integration with Worker Thread Pool, Record-driven parameterized tests, Pattern
  Matching assertions, Unified Extension Model), following best practices (FastCSV
  RFC 4180 compliance, JSpecify nullability contracts, deterministic nested ordering),
  implementing workarounds (pinning mitigation with ReentrantLock, CSV data migration,
  extension API migration from getOrComputeIfAbsent), and avoiding anti-patterns (synchronized
  blocks with Virtual Threads, ForkJoinPool for I/O tests, mutable test data, legacy
  @RunWith usage). Use when testing in Java 21 environments, building high-concurrency
  integration test suites, modernizing from JUnit 5.x, or testing Java 21 features
  (Records, Pattern Matching, Virtual Threads).
name: implementing-junit6-java21
version: 1.0.0
---

# Implementing JUnit 6.0.1 in Java 21

## Overview

JUnit 6.0.1 unifies versioning across Platform, Jupiter, and Vintage artifacts, eliminating dependency conflicts. It mandates Java 17+ but optimizes for Java 21 features: Virtual Threads for massive parallel test execution, Records for immutable test data, Pattern Matching for sealed hierarchy assertions, and JSpecify nullability contracts. The framework removes legacy runners, integrates JFR natively, and switches to FastCSV for RFC 4180-compliant CSV parsing. This skill provides procedural knowledge for implementing production-ready JUnit 6.0.1 test suites following proven patterns, best practices, and workarounds while avoiding common anti-patterns.

## When to Use

Use this skill when:
- Testing in Java 21 environments requiring high concurrency
- Building integration test suites with blocking I/O operations
- Migrating from JUnit 5.x to JUnit 6.0.1
- Testing Java 21 language features (Records, Pattern Matching, Virtual Threads)
- Building data-oriented test suites with immutable test data

**Input format**: Java 21 project structure, business logic to test, Maven or Gradle build system
**Expected output**: Production-ready JUnit 6.0.1 test suite following enterprise patterns, Virtual Thread integration configured, best practices applied, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- Java 21+ installed and configured (`java -version` must show 21 or later)
- Maven or Gradle build system configured
- Understanding of JUnit 5 basics (for migration scenarios)
- Business logic code to test

## Execution Steps

### Step 1: Dependency Configuration

JUnit 6.0.1 uses unified versioning via BOM. All artifacts (Platform, Jupiter, Vintage) share the same version string, eliminating version drift.

**Maven Configuration**:
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.junit</groupId>
            <artifactId>junit-bom</artifactId>
            <version>6.0.1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.platform</groupId>
        <artifactId>junit-platform-launcher</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Gradle Configuration**:
```kotlin
dependencies {
    testImplementation(platform("org.junit:junit-bom:6.0.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

**Best Practice**: Use BOM for unified versioning. Include `junit-platform-launcher` as testRuntimeOnly (required since `junit-platform-runner` is removed).
**Anti-Pattern**: ❌ Mixing different JUnit versions (Platform 6.0.1 with Jupiter 5.x) causing dependency conflicts

### Step 2: Virtual Thread Integration (Java 21 Pattern)

JUnit 6.0.1 introduces Worker Thread Pool executor service, optimized for Virtual Threads on Java 21. This enables "thread-per-test" model scaling to thousands of concurrent tests.

**Configuration** (`src/test/resources/junit-platform.properties`):
```properties
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.config.strategy = fixed
junit.jupiter.execution.parallel.config.fixed.parallelism = 1000
junit.jupiter.execution.parallel.config.executor-service = worker_thread_pool
```

**Template Reference**: See `templates/virtual-thread-config.template`, `templates/worker-thread-pool-config.template`

**Best Practice**: Use `worker_thread_pool` for I/O-heavy test suites. Virtual Threads unmount during blocking I/O, allowing massive parallelism without exhausting OS threads.
**Anti-Pattern**: ❌ Using ForkJoinPool for blocking I/O tests (causes thread starvation, reduced throughput)

### Step 3: Pinning Detection and Mitigation

Virtual Threads pin to OS carrier threads when blocking occurs inside synchronized blocks or native methods, preventing unmounting and degrading performance.

**Detection**: Run tests with JVM flag to identify pinning:
```bash
-Djdk.tracePinnedThreads=full
```

**Mitigation Pattern**: Replace synchronized with ReentrantLock:
```java
// BAD: Synchronized causes pinning
synchronized void setupDatabase() {
    blockingIO();
}

// GOOD: ReentrantLock allows unmounting
private final ReentrantLock lock = new ReentrantLock();

void setupDatabase() {
    lock.lock();
    try {
        blockingIO(); // Virtual thread unmounts here
    } finally {
        lock.unlock();
    }
}
```

**Best Practice**: Monitor pinning events using JFR, replace synchronized with ReentrantLock in I/O paths
**Anti-Pattern**: ❌ Blocking I/O in synchronized blocks (causes pinning, prevents unmounting). ❌ Ignoring pinning warnings

### Step 4: Record-Driven Parameterized Tests

Java 21 Records provide immutable, self-documenting test data carriers with automatic toString() for display names.

**Pattern**: Define Record for test scenario:
```java
record PricingScenario(
    String name,
    BigDecimal basePrice,
    CustomerType type,
    BigDecimal expectedTotal
) {
    @Override
    public String toString() { return name; }
}

static Stream<PricingScenario> scenarios() {
    return Stream.of(
        new PricingScenario("Regular", new BigDecimal("100.00"), CustomerType.REGULAR, new BigDecimal("100.00")),
        new PricingScenario("VIP", new BigDecimal("100.00"), CustomerType.VIP, new BigDecimal("90.00"))
    );
}

@ParameterizedTest
@MethodSource("scenarios")
void calculatePrice(PricingScenario scenario) {
    var result = PricingService.calculate(scenario.basePrice(), scenario.type());
    assertEquals(scenario.expectedTotal(), result);
}
```

**Template Reference**: See `templates/record-parameterized-test.template`

**Best Practice**: Records for immutable test scenarios, automatic toString() eliminates need for custom display names
**Anti-Pattern**: ❌ Mutable test data objects (causes flaky tests in concurrent execution). ❌ Verbose static inner classes for test data

### Step 5: Pattern Matching in Assertions

Java 21 switch expressions enable declarative assertions for sealed hierarchies, eliminating nested if-else chains.

**Pattern**: Use switch expressions for sealed type assertions:
```java
sealed interface Result permits Success, Failure {}
record Success(String id) implements Result {}
record Failure(String error) implements Result {}

@Test
void processResult() {
    Result result = service.process();
    
    String message = switch (result) {
        case Success(var id) -> "OK: " + id;
        case Failure(var err) -> "Error: " + err;
    };
    
    assertTrue(message.startsWith("OK"));
}
```

**Pattern Matching for instanceof**:
```java
// OLD: Nested if-else with casting
if (obj instanceof MyType) {
    MyType m = (MyType) obj;
    assertEquals("val", m.val());
}

// NEW: Pattern matching with binding
if (obj instanceof MyType m) {
    assertEquals("val", m.val());
}
```

**Template Reference**: See `templates/pattern-matching-assertion.template`

**Best Practice**: Declarative switch-based assertions, pattern matching eliminates casting boilerplate
**Anti-Pattern**: ❌ Deeply nested if-else with instanceof checks and explicit casting

### Step 6: Unified Extension Model Migration

JUnit 6.0.1 deprecates `getOrComputeIfAbsent` in favor of `computeIfAbsent`, aligning with standard Java Map API and enforcing stricter type safety.

**Migration Pattern**:
```java
// OLD: getOrComputeIfAbsent (deprecated)
Object value = store.getOrComputeIfAbsent(key, k -> computeValue());

// NEW: computeIfAbsent (type-safe)
String value = store.computeIfAbsent(key, String.class, k -> computeValue());
```

**Template Reference**: See `templates/unified-extension-model.template`

**Best Practice**: Type-safe store operations prevent ClassCastExceptions when extensions collide on store keys
**Anti-Pattern**: ❌ Using deprecated getOrComputeIfAbsent (removed in future versions). ❌ Lenient generics causing runtime ClassCastException

### Step 7: FastCSV Migration

JUnit 6.0.1 switches from univocity-parsers to FastCSV, enforcing strict RFC 4180 compliance. Tests with loose CSV formatting may break.

**Compliance Requirements**:
- Quoted fields must use double quotes
- Escaped quotes within fields: `""` (double double-quote)
- Newlines within fields must be quoted
- Trailing commas are not allowed

**Migration Checklist**:
1. Audit all `@CsvSource` and `@CsvFileSource` annotations
2. Verify quoted fields use proper escaping
3. Check for unescaped quotes within fields
4. Validate newline handling in multi-line fields

**Template Reference**: See `templates/fastcsv-migration.template`

**Best Practice**: Strict RFC 4180 formatting ensures correctness and portability
**Anti-Pattern**: ❌ Loose CSV escaping (univocity tolerance no longer works). ❌ Incorrect quote escaping causing test failures

### Step 8: Deterministic Nested Test Order

JUnit 6.0.1 introduces deterministic execution order for `@Nested` classes, but the order is intentionally non-obvious to prevent reliance on implicit sequencing.

**Pattern**: Use `@TestClassOrder` for explicit ordering:
```java
@TestClassOrder(ClassOrderer.OrderAnnotation.class)
class TestSuite {
    @Nested
    @Order(1)
    class FirstTestGroup { }
    
    @Nested
    @Order(2)
    class SecondTestGroup { }
}
```

**Best Practice**: Explicit ordering when test sequence matters, prevents flaky tests from shared state
**Anti-Pattern**: ❌ Relying on implicit nested order (order is deterministic but non-obvious). ❌ Shared mutable state between nested classes

### Step 9: org.junit.start Module (JEP 458)

JUnit 6.0.1 introduces `org.junit.start` module for single-file source-code programs, enabling rapid prototyping without build configuration.

**Pattern**: Minimalist single-file test:
```java
// HelloTests.java
import module org.junit.start;

void main() {
    JUnit.run();
}

@Test
void stringLength() {
    Assertions.assertEquals(11, "Hello JUnit".length());
}
```

**Template Reference**: See `templates/junit-start-module.template`

**Best Practice**: Rapid prototyping for learning exercises, algorithm testing without Maven/Gradle overhead
**Use Case**: Single-file test programs, educational examples, quick validation

### Step 10: JSpecify Nullability

JUnit 6.0.1 adopts JSpecify annotations throughout public API, enforcing null-safety contracts at compile-time and runtime.

**Impact**: Passing null to non-nullable parameters now fails early with clear error messages. Extension code must handle nullability explicitly.

**Migration**: Review extension code for null handling:
```java
// Extension code must respect nullability
void beforeTest(ExtensionContext context) {
    // context is non-null (JSpecify contract)
    // No need for null checks, but IDE will warn if null passed
}
```

**Best Practice**: Explicit nullability contracts prevent undefined behavior, align with Kotlin 2.x interoperability
**Anti-Pattern**: ❌ Passing null to non-nullable parameters (causes runtime failures). ❌ Ignoring IDE nullability warnings

## Real-World Examples

### Example 1: Virtual Integration Test Suite

**Context**: Database integration tests requiring high concurrency without thread pool exhaustion.

**Configuration** (`junit-platform.properties`):
```properties
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.config.strategy = fixed
junit.jupiter.execution.parallel.config.fixed.parallelism = 1000
junit.jupiter.execution.parallel.config.executor-service = worker_thread_pool
```

**Test Class**:
```java
@Execution(ExecutionMode.CONCURRENT)
class UserDatabaseTest {
    private static final Semaphore DB_CONNECTIONS = new Semaphore(50);
    
    @Test
    void createUser(UserRepo repo) {
        DB_CONNECTIONS.acquire();
        try {
            var user = repo.save(new User("test", "test@example.com"));
            assertNotNull(user.id());
        } finally {
            DB_CONNECTIONS.release();
        }
    }
}
```

**Key Points**: Worker Thread Pool enables Virtual Threads, Semaphore limits DB connections without blocking threads, unmounting occurs during blocking I/O.

### Example 2: Record-Driven Pricing Test

**Context**: Business rule testing with multiple pricing scenarios requiring immutability and clean structure.

**Test Class**:
```java
class PricingTest {
    record PricingScenario(String name, BigDecimal base, CustomerType type, BigDecimal expected) {
        @Override
        public String toString() { return name; }
    }
    
    static Stream<PricingScenario> scenarios() {
        return Stream.of(
            new PricingScenario("Regular", new BigDecimal("100"), CustomerType.REGULAR, new BigDecimal("100")),
            new PricingScenario("VIP", new BigDecimal("100"), CustomerType.VIP, new BigDecimal("90"))
        );
    }
    
    @ParameterizedTest
    @MethodSource("scenarios")
    void calculatePrice(PricingScenario scenario) {
        var result = PricingService.calculate(scenario.base(), scenario.type());
        assertEquals(scenario.expected(), result);
    }
}
```

**Key Points**: Record immutability prevents test data mutation, automatic toString() provides display names, clean test structure without boilerplate.

## Error Handling

**Common Migration Errors**:

1. **Legacy Runner Removal**: `@RunWith(JUnitPlatform.class)` no longer exists
   - **Resolution**: Remove annotation, configure IDE/build tool to use native JUnit Platform launcher

2. **CSV Format Issues**: FastCSV strict compliance causes test failures
   - **Resolution**: Audit CSV data, fix quote escaping, ensure RFC 4180 compliance

3. **Extension API Migration**: `getOrComputeIfAbsent` compilation errors
   - **Resolution**: Replace with `computeIfAbsent`, add explicit type parameter

4. **Pinning Detection**: Virtual Threads not unmounting during I/O
   - **Resolution**: Run with `-Djdk.tracePinnedThreads=full`, replace synchronized with ReentrantLock

5. **Dependency Conflicts**: Version drift between Platform and Jupiter
   - **Resolution**: Use unified BOM (junit-bom:6.0.1) for all artifacts

## Security and Guidelines

**CRITICAL**: Never hardcode sensitive information:
- ❌ No database credentials in test code
- ❌ No API keys or tokens in test fixtures
- ✅ Use external configuration files or environment variables
- ✅ Isolate test data from production data

**Operational Constraints**:
- Test data must be isolated (no shared mutable state)
- Resource cleanup required (connections, file handles)
- Virtual Thread limits: Monitor carrier thread pool size (defaults to CPU cores)

## Dependencies

This skill requires:
- `org.junit:junit-bom:6.0.1`: Unified BOM for all JUnit artifacts
- `java>=21`: Java 21+ runtime for Virtual Threads and modern features

**Note**: For API-based deployments, all dependencies must be pre-installed in the execution environment.

## Performance Considerations

- **Virtual Threads**: Enable massive parallelism for I/O-bound tests (thousands of concurrent tests)
- **Worker Thread Pool**: Prevents ForkJoinPool starvation in blocking I/O scenarios
- **Pinning Mitigation**: Monitor and eliminate pinning to maximize Virtual Thread benefits
- **Record Immutability**: Prevents flaky tests from concurrent data mutation

## Related Resources

For extensive reference materials, see:
- `templates/virtual-thread-config.template`: Virtual Thread configuration patterns
- `templates/record-parameterized-test.template`: Record-based test data patterns
- `templates/pattern-matching-assertion.template`: Pattern matching assertion patterns
- `templates/worker-thread-pool-config.template`: Worker Thread Pool executor configuration
- `templates/unified-extension-model.template`: Extension API migration patterns
- `templates/fastcsv-migration.template`: CSV migration checklist
- `templates/junit-start-module.template`: Single-file test patterns

## Notes

- JUnit 6.0.1 requires Java 17+ but optimizes for Java 21
- Worker Thread Pool is experimental in 6.0.1 but recommended for I/O-heavy suites
- FastCSV migration may break tests with loose CSV formatting (correctness fix)
- JSpecify nullability enforcement may cause new warnings in extension code
- `org.junit.start` module requires Java 21+ with JEP 458 support

