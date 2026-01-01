---
dependencies:
- java>=21
description: Implements Java 21 applications by applying patterns (Virtual Threads
  for I/O concurrency, Structured Concurrency for task coordination, Scoped Values
  for context propagation, Data-Oriented Programming with Records/Sealed/Pattern Matching,
  Sequenced Collections for ordered data), following best practices (synchronous thread-per-request,
  ReentrantLock over synchronized, Semaphore throttling, Scoped Values over ThreadLocal),
  implementing workarounds (pinning mitigation, ThreadLocal migration, Records vs
  JPA entities), and avoiding anti-patterns (virtual thread pooling, blocking I/O
  in synchronized, ThreadLocal abuse, mutable records). Use when migrating to Java
  21, building high-concurrency I/O applications, modernizing legacy code, or replacing
  reactive frameworks with synchronous code.
name: implementing-java-21-architecture
version: 1.0.0
---

# Implementing Java 21 Architecture

## Overview

Java 21 LTS enables synchronous I/O at scale via Virtual Threads, eliminating the need for reactive frameworks. Key features include Virtual Threads (JEP 444) for millions of concurrent operations, Structured Concurrency (JEP 453) for task coordination, Scoped Values (JEP 446) for context propagation, enhanced Pattern Matching with Records/Sealed Types, and Sequenced Collections (JEP 431) for ordered data access. This skill provides procedural knowledge for implementing production-ready Java 21 applications following proven patterns, best practices, and workarounds while avoiding common anti-patterns.

## When to Use

Use this skill when:
- Migrating from Java 8/11/17 to Java 21
- Building high-throughput I/O-bound applications
- Replacing reactive frameworks (WebFlux, RxJava) with synchronous code
- Modernizing legacy codebases with modern Java patterns

**Input format**: Java codebase, business requirements, I/O-bound workloads
**Expected output**: Production-ready Java 21 implementation following enterprise patterns, best practices applied, workarounds documented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- Java 21+ installed and configured (`java -version` must show 21 or later)
- Maven or Gradle build system
- Understanding of basic Java concurrency concepts

## Execution Steps

### Step 1: Virtual Threads Pattern

Virtual Threads enable millions of concurrent operations with minimal overhead, perfect for I/O-bound workloads.

**Pattern**: Use Virtual Threads for all blocking I/O operations:

```java
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
executor.submit(() -> blockingIO());
```

**Best Practice**: 
- No pooling required (virtual threads are lightweight and disposable)
- Use Semaphore for concurrency limits if needed
- Prefer synchronous code over reactive patterns

**Anti-Pattern**: ❌ Pooling virtual threads (they're disposable, pooling defeats the purpose). ❌ Using reactive frameworks unnecessarily (Virtual Threads make synchronous code scalable).

**Workaround**: Use Semaphore for throttling when needed:

```java
Semaphore semaphore = new Semaphore(1000);
executor.submit(() -> {
    semaphore.acquire();
    try {
        blockingIO();
    } finally {
        semaphore.release();
    }
});
```

### Step 2: Pinning Mitigation

Virtual threads unmount during blocking operations, but pinning occurs when blocking happens inside synchronized blocks or native methods.

**Pattern**: Use ReentrantLock instead of synchronized for any blocking I/O path:

```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    blockingIO(); // Virtual thread unmounts here
} finally {
    lock.unlock();
}
```

**Best Practice**: 
- Replace synchronized with ReentrantLock in I/O paths
- Monitor pinning events using JFR

**Anti-Pattern**: ❌ Blocking I/O in synchronized blocks (causes pinning, prevents unmounting). ❌ Ignoring pinning warnings.

**Workaround**: Use JFR to detect pinning:

```bash
-XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints
# Monitor jdk.VirtualThreadPinned event
```

### Step 3: Structured Concurrency (Preview)

Structured Concurrency ensures child tasks complete before parent scope closes, preventing resource leaks and orphaned tasks.

**Pattern**: Use StructuredTaskScope for coordinated task execution:

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<String> orders = scope.fork(() -> fetchOrders());
    scope.join();
    scope.throwIfFailed();
    return combine(user.resultNow(), orders.resultNow());
}
```

**Best Practice**: 
- Always use try-with-resources for scope management
- Choose ShutdownOnFailure or ShutdownOnSuccess based on requirements

**Anti-Pattern**: ❌ Unstructured ExecutorService usage (allows orphaned tasks). ❌ Not using try-with-resources (resource leaks).

### Step 4: Scoped Values (Preview)

Scoped Values provide thread-local-like functionality without the memory overhead of ThreadLocal with millions of threads.

**Pattern**: Replace ThreadLocal with Scoped Values:

```java
private static final ScopedValue<User> USER_CONTEXT = ScopedValue.newInstance();

ScopedValue.where(USER_CONTEXT, user).run(() -> {
    // Access USER_CONTEXT.get() anywhere in call stack
    processRequest();
});
```

**Best Practice**: 
- Use Scoped Values for context propagation
- Migrate from ThreadLocal gradually

**Anti-Pattern**: ❌ ThreadLocal with millions of threads (memory overhead). ❌ Not migrating ThreadLocal to Scoped Values.

**Workaround**: Gradual migration pattern:

```java
// Legacy ThreadLocal
private static final ThreadLocal<User> LEGACY_CONTEXT = new ThreadLocal<>();

// New Scoped Value
private static final ScopedValue<User> NEW_CONTEXT = ScopedValue.newInstance();

// Bridge during migration
ScopedValue.where(NEW_CONTEXT, user).run(() -> {
    LEGACY_CONTEXT.set(user);
    try {
        legacyCode();
    } finally {
        LEGACY_CONTEXT.remove();
    }
});
```

### Step 5: Data-Oriented Programming

Java 21 enhances Records, Sealed Types, and Pattern Matching for expressive data modeling.

**Pattern**: Use sealed interfaces with Records and pattern matching:

```java
sealed interface Result permits Success, Failure {}
record Success(String id) implements Result {}
record Failure(String error) implements Result {}

String process(Result result) {
    return switch (result) {
        case Success(var id) -> "OK: " + id;
        case Failure(var err) -> "Error: " + err;
    };
}
```

**Best Practice**: 
- Use Records for DTOs and immutable data
- Use POJOs for JPA entities (Records are immutable)
- Leverage sealed types for exhaustive pattern matching

**Anti-Pattern**: ❌ Mutable records (violates immutability contract). ❌ Mega-switches without sealed types (no exhaustiveness guarantee). ❌ Using Records as JPA entities (immutability conflicts with JPA requirements).

**Workaround**: Records vs JPA entities:

```java
// DTO (use Record)
public record UserDto(Long id, String name) {}

// JPA Entity (use POJO)
@Entity
public class User {
    @Id
    private Long id;
    private String name;
    // Getters, setters, no-arg constructor required
}
```

### Step 6: Sequenced Collections

Sequenced Collections provide consistent access patterns for ordered collections.

**Pattern**: Use SequencedCollection interface methods:

```java
SequencedCollection<String> list = new LinkedHashSet<>();
list.getFirst(); // Instead of list.iterator().next()
list.getLast();  // Instead of list.stream().reduce((a, b) -> b).orElse(null)
list.reversed(); // Reverse view without copying
```

**Best Practice**: 
- Use SequencedCollection interface for consistent API
- Prefer LinkedHashSet/LinkedHashMap for ordered collections

**Anti-Pattern**: ❌ Inconsistent access patterns (get(0) vs iterator().next()). ❌ Manual reverse operations (use reversed() view).

### Step 7: Performance (ZGC)

Generational ZGC provides low-latency garbage collection suitable for high-throughput applications.

**Pattern**: Enable generational ZGC:

```bash
-XX:+UseZGC -XX:+ZGenerational
```

**Best Practice**: 
- Enable generational ZGC for low-latency requirements
- Monitor GC metrics with JFR

## Anti-Patterns

- ❌ Pooling virtual threads (they're disposable)
- ❌ Blocking I/O in synchronized blocks (causes pinning)
- ❌ ThreadLocal with millions of threads (use Scoped Values)
- ❌ Mutable records (violates immutability contract)
- ❌ Mega-switches without sealed types (no exhaustiveness guarantee)
- ❌ Using Records as JPA entities (immutability conflicts with JPA)

## Workarounds

- **Pinning Detection**: Use JFR `jdk.VirtualThreadPinned` event to identify pinning
- **ThreadLocal Migration**: Replace with Scoped Values gradually using bridge pattern
- **Records vs JPA**: Use Records for DTOs, keep POJOs for JPA entities

## Examples

### Example 1: HTTP Service with Virtual Threads

```java
@RestController
public class UserController {
    private final ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
    private final UserService userService;
    
    @GetMapping("/users/{id}")
    public CompletableFuture<User> getUser(@PathVariable String id) {
        return CompletableFuture.supplyAsync(() -> userService.findById(id), executor);
    }
}
```

### Example 2: Payment Result with Sealed Types

```java
sealed interface PaymentResult permits Success, Failure, Pending {}
record Success(String transactionId) implements PaymentResult {}
record Failure(String error) implements PaymentResult {}
record Pending() implements PaymentResult {}

String process(PaymentResult result) {
    return switch (result) {
        case Success(var id) -> "Processed: " + id;
        case Failure(var err) -> "Error: " + err;
        case Pending() -> "Waiting...";
    };
}
```

## Migration Guide

- **Upgrade Path**: Java 8/11/17 → Java 21
- **Common Blockers**: 
  - Deprecated APIs (use replacement APIs from newer JDK versions)
  - Third-party libraries (check Java 21 compatibility)
- **Tooling**: 
  - Maven: `<maven.compiler.source>21</maven.compiler.source>`
  - Gradle: `sourceCompatibility = JavaVersion.VERSION_21`

