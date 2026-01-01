---
dependencies:
- python>=3.9
- requests>=2.31.0
- axios>=1.6.0
description: Implements Kualitee Test Management integration by applying proven patterns
  (traceability pattern, AI augmentation, module/build granularity, API integration),
  following best practices (requirement-to-defect linkage, Build/Module segmentation,
  active reporting governance), implementing workarounds (multi-platform Build separation,
  API status synchronization), and avoiding anti-patterns (multi-platform scenario
  duplication, passive reporting, inadequate test data management). Use when implementing
  test management integration, setting up API automation, managing multi-platform
  projects, configuring traceability workflows, or integrating with CI/CD pipelines.
name: implementing-kualitee-test-management
version: 1.0.0
---

# Implementing Kualitee Test Management

## Overview

Implements Kualitee Test Management integration for centralized quality assurance workflows. Kualitee provides integrated Requirement Management, Test Case execution, and Defect Management within a single platform, enabling end-to-end traceability from requirements through test execution to defect resolution. This skill provides procedural knowledge for establishing traceability patterns, API integration for automation frameworks, multi-platform project management, and critical operational practices while avoiding common anti-patterns.

## When to Use

Use this skill when:
- Implementing test management integration with automation frameworks (Selenium, Cypress, Appium, Playwright)
- Setting up API automation for real-time test execution status synchronization
- Managing multi-platform projects (iOS/Android, web/mobile) with shared requirements
- Configuring traceability workflows for compliance and auditability
- Integrating with CI/CD pipelines (CircleCI, Jenkins, GitHub Actions)
- Establishing centralized quality ledger for requirements, tests, and defects

**Input format**: Kualitee domain setup, API token, Project/Build/Module structure, automation framework (Python/Node.js/BDD)

**Expected output**: Production-ready Kualitee integration following proven patterns, best practices applied, workarounds implemented, anti-patterns avoided

## Prerequisites

Before using this skill, ensure:
- Kualitee domain is set up and accessible
- API token generated via User Profile > Token > API Token
- Project, Build, and Module structure created in Kualitee
- Test Cases created and added to active execution cycle
- Automation framework available (Python requests, Node.js Axios, BDD hooks)
- Test Case IDs and Project IDs extracted from Test Lab > Test Execution interface

## Execution Steps

### Step 1: Traceability Pattern Implementation

Establish bidirectional linkage: Requirements → Test Cases → Defects. This creates an auditable quality ledger essential for compliance.

**Implementation Approach**:
1. Link all Test Cases to Requirements in Kualitee interface
2. When defects are logged, link to failed Test Case and originating Requirement
3. Use traceability matrix to track coverage and impact

**Key Benefit**: Enables instant impact assessment when requirements change. Generate custom reports showing affected tests and defects.

**Best Practice**: Maintain requirement-to-test ratio of 1:N (one requirement, multiple test cases) for comprehensive coverage.

### Step 2: AI Augmentation Pattern (Hootie)

Leverage Kualitee's AI copilot for foundational test case generation, allowing human testers to focus on complex scenarios.

**Strategic Application**:
- Use Hootie for generating simple, straightforward test cases (up to 80% coverage)
- Human testers validate AI-generated cases and design complex exploratory scenarios
- AI-generated cases integrate directly with external automation frameworks

**Best Practice**: Generate basic smoke tests and unit tests via AI, reserve human expertise for critical business paths and edge cases.

**Limitation**: AI features are most effective for simple tests. Complex validation requires human oversight.

### Step 3: Structural Best Practice - Module and Build Granularity

Organize projects using hierarchical structure: Projects → Builds → Modules.

**Modules**: Logical groupings for feature sets, linking test scenarios to requirements.

**Builds**: Manage software versions under test. Critical for version control and release management.

**Best Practice**: 
- Create distinct Builds for each platform and version (e.g., "V1.0.0 iOS Build 101", "V1.0.0 Android Build 57")
- Use Modules to group related features and requirements
- Associate test suites with specific Builds for accurate version tracking

**Anti-Pattern**: ❌ Using Test Scenarios to differentiate platforms. This causes duplication and maintenance overhead.

### Step 4: API Integration Pattern - Real-time Status Synchronization

Use Kualitee's Independent API for tool-agnostic automation integration.

**Core Integration Pattern**:
- POST request to `https://apiss.kualitee.com/api/v2/test_case_execution/change_status`
- Authentication via API token in request payload
- Status codes: 1=Passed, 2=Failed, 4=Blocked

**Parameter Extraction**:
1. Navigate to Test Lab > Test Execution
2. Click Action Icon on target test case
3. Extract: Project ID, Test Case ID, Status code mappings

**Integration Best Practice**: Place API call in AFTER Hook (or tearDown/afterEach) of automation framework. Ensures status update occurs only after test execution completes and final result is captured.

See templates: `api-status-update-python.template`, `api-status-update-nodejs.template`, `bdd-after-hook.template`

### Step 5: Multi-Platform Workaround - Build/Module Segmentation

For mobile applications (iOS/Android) or multi-platform software sharing core functionality:

**Correct Structural Pattern**:
1. **Centralize Requirements and Scenarios**: Define user goal once as Test Scenario (e.g., "User Login")
2. **Separate Test Case Implementation**: Create platform-specific Test Cases (e.g., "TC-001-iOS: Verify FaceID login", "TC-001-Android: Verify fingerprint login")
3. **Use Builds for Platform Differentiation**: Create distinct Builds per platform/version within single project
4. **Targeted Execution**: Assign platform-specific Test Cases to corresponding Builds. Filter execution cycle by active Build to isolate results

**Anti-Pattern**: ❌ Managing both platforms in single project using Test Scenarios for platform differentiation. Results in scenario duplication and confusing results.

## Patterns

### Pattern 1: Traceability Pattern (Requirement to Defect Linkage)

**Goal**: Establish end-to-end auditability from requirements through test execution to defect resolution.

**Implementation**:
- Link Test Cases to Requirements during test design
- Link Defects to failed Test Cases and originating Requirements during defect logging
- Generate traceability reports for impact assessment

**Compliance Benefit**: Provides verifiable audit trail for regulated environments (healthcare, finance).

**Real-World Impact**: Healthcare customer achieved 44% testing speed increase by eliminating version control problems through centralized traceability.

### Pattern 2: API Integration Pattern (Real-time Status Synchronization)

**Goal**: Synchronize test execution results from external automation frameworks to Kualitee Test Lab in real-time.

**Implementation**:
- Use POST endpoint: `https://apiss.kualitee.com/api/v2/test_case_execution/change_status`
- Send form-encoded payload with: token, project_id, test_case_id, status
- Place API call in AFTER Hook of automation framework

**Key Benefit**: Enables Kualitee to function as real-time quality gate in CI/CD pipelines. Build fails immediately if critical tests report 'Failed'.

**Flexibility**: Tool-agnostic approach allows changing automation technologies without overhauling synchronization logic.

### Pattern 3: Build/Module Segmentation Pattern (Multi-Platform Management)

**Goal**: Manage multi-platform projects without scenario duplication or maintenance overhead.

**Implementation**:
- Reserve Test Scenarios for high-level, platform-agnostic functional goals
- Use Builds for platform-specific execution tracking and version management
- Create distinct Test Cases per platform implementing shared scenarios
- Filter execution cycles by Build to isolate platform results

**Structural Strategy**: Decouple high-level functionality (Scenario) from platform-specific deployment (Build).

## Best Practices

### Best Practice 1: Requirement-to-Defect Linkage

**Bidirectional Traceability**: Maintain links from Requirements forward to Test Cases, and backward from Defects to Test Cases and Requirements.

**Implementation**:
- Link all Test Cases to Requirements during creation
- When logging defects, always link to failed Test Case and originating Requirement
- Use traceability matrix for coverage analysis

**Benefit**: Enables proactive risk mitigation by prioritizing bug fixes based on requirement criticality.

### Best Practice 2: Build/Module Granularity

**Clear Version and Platform Separation**: Use Builds for version control and Modules for feature organization.

**Implementation**:
- Create distinct Builds for each platform and version combination
- Use Modules to group related features and requirements
- Associate test suites with specific Builds for accurate tracking

**Benefit**: Supports effective Continuous Delivery and Release Management workflows with precise version tracking.

### Best Practice 3: Active Reporting Governance

**Custom Dashboards and Scheduled Reports**: Configure personalized dashboards and custom reports beyond default settings.

**Implementation**:
- Create personalized dashboards for testers, developers, and managers
- Configure custom reports with savable templates
- Schedule reports for automated delivery
- Monitor real-time quality metrics and identify bottlenecks

**Benefit**: Transforms Kualitee from repository into proactive strategic analysis platform. Prevents missed KPIs and delayed quality strategy optimization.

**Anti-Pattern**: ❌ Relying on out-of-the-box reports. Prevents real-time visibility and continuous improvement.

## Workarounds

### Workaround 1: Multi-Platform Complexity (Module/Build Segmentation)

**Problem**: Managing iOS and Android apps in single project causes scenario duplication and confusing results when using Test Scenarios for platform differentiation.

**Solution**: Use Build/Module segmentation pattern:
- Centralize Requirements and Scenarios at planning layer (platform-agnostic)
- Separate Test Case implementation per platform
- Use Builds for version and platform differentiation
- Filter execution cycles by Build to isolate platform results

**Result**: Eliminates scenario duplication, reduces maintenance overhead, provides clear platform-specific execution tracking.

### Workaround 2: Agile Change Management (Real-time Impact Assessment)

**Problem**: In dynamic Agile environments, requirements constantly evolve, making it difficult to assess impact on testing and release quality.

**Solution**: Utilize traceability and reporting capabilities:
- Link requirements to test cases (established during test design)
- Generate custom reports showing affected tests when requirements change
- Share comprehensive impact information with development and business analysis teams
- Enable sprint adjustments without compromising quality

**Result**: Provides instant visibility into change impact, supports informed decision-making for sprint planning.

## Anti-Patterns

### Anti-Pattern 1: Multi-Platform Project Anti-Pattern (Scenario Duplication)

**Problem**: Attempting to manage divergent mobile applications (iOS/Android) in single project by using Test Scenarios to differentiate platform execution.

**Symptoms**:
- Duplication of Test Scenarios
- Confusing results (test case section appears blank when viewed in context of different platform)
- High maintenance overhead
- User experience friction described as "extremely frustrating"

**Why It's Problematic**: Misaligns with Kualitee's architecture. Test Scenarios should define high-level, platform-agnostic functional goals. Using Scenarios for platform-specific execution tracking creates hidden scalability constraints.

**Correct Approach**: Use Build/Module Segmentation Pattern (see Pattern 3, Workaround 1). Differentiate execution using distinct Builds or Modules within single project. Decouple high-level functionality from platform-specific deployment.

### Anti-Pattern 2: Passive Management and Reporting Anti-Pattern

**Problem**: Passive acceptance of default reporting settings, preventing Kualitee from functioning as proactive management tool.

**Symptoms**:
- Missing real-time quality metrics
- Delayed identification of bottlenecks
- Inability to optimize QA strategies
- Limited visibility into testing progress

**Why It's Problematic**: Kualitee provides Personalized Dashboards and Customizable Reporting features, but failing to leverage them prevents continuous improvement and limits efficiency gains.

**Correct Approach**: Implement Active Reporting Governance (see Best Practice 3). Configure personalized dashboards, create custom report templates, schedule automated reports. Actively govern data visibility for proactive monitoring.

### Anti-Pattern 3: Inadequate Test Data Management

**Problem**: Treating test data preparation as entirely external, decoupled activity.

**Symptoms**:
- Missed defects due to insufficient test data
- Unrealistic test coverage assessment
- Incomplete scenario validation

**Why It's Problematic**: If test data is insufficient or irrelevant, validation fails to catch defects and coverage assessment becomes unreliable.

**Correct Approach**: Define test data requirements explicitly within Kualitee's test case steps. Integrate external data generation tools to create large volumes of relevant data. Ensure thorough coverage of all possible scenarios. Integrate data strategy into test planning within the TM tool.

## Code Templates

### Python API Status Update

See `templates/api-status-update-python.template` for complete pattern.

**Key Elements**:
- POST request to change_status endpoint
- Form-encoded payload (project_id, test_case_id, status, token)
- Error handling for invalid IDs or tokens
- Status code mapping (1=Passed, 2=Failed, 4=Blocked)

### Node.js API Status Update

See `templates/api-status-update-nodejs.template` for complete pattern.

**Key Elements**:
- Axios POST request with form encoding
- URLSearchParams for data formatting
- Error handling with response data extraction

### BDD Hook Integration

See `templates/bdd-after-hook.template` for complete pattern.

**Key Elements**:
- after_scenario hook implementation
- Test Case ID extraction from scenario tags
- Status determination from framework outcome
- API call placement in cleanup phase

### Build/Module Segmentation

See `templates/build-module-segmentation.template` for structural pattern.

**Key Elements**:
- Build naming convention for platform/version
- Module organization strategy
- Execution cycle filtering approach

## Error Handling

**API Authentication Failures**:
- Verify API token is valid and not expired
- Check token generation via User Profile > Token > API Token
- Ensure token is included in request payload

**Invalid Test Case or Project ID**:
- Extract IDs from Test Lab > Test Execution > Action Icon popup
- Verify IDs match active execution cycle
- Confirm test case is assigned to correct Build

**Status Update Failures**:
- Verify status code mapping (1=Passed, 2=Failed, 4=Blocked)
- Check network connectivity to Kualitee domain
- Validate form-encoded payload format

**Multi-Platform Execution Issues**:
- Ensure Build filtering is applied during execution cycle creation
- Verify platform-specific Test Cases are assigned to correct Builds
- Check that Scenarios remain platform-agnostic

## Security and Guidelines

**CRITICAL**: Never hardcode sensitive information:
- ❌ No API tokens in code
- ❌ No credentials in SKILL.md or templates
- ✅ Use environment variables or secure credential management
- ✅ Route sensitive operations through secure channels

**Operational Constraints**:
- API tokens must be generated per user account
- Test Case and Project IDs are project-specific
- Status updates require active execution cycle

## Dependencies

This skill requires the following packages (listed in frontmatter):
- `python>=3.9`: For Python automation framework integration
- `requests>=2.31.0`: For HTTP POST requests to Kualitee API
- `axios>=1.6.0`: For Node.js automation framework integration

**Note**: For API-based deployments, all dependencies must be pre-installed in the execution environment. The skill cannot install packages at runtime.

## Performance Considerations

- API calls should be placed in AFTER Hooks to avoid blocking test execution
- Batch status updates when possible (if API supports batching)
- Cache Project IDs and Test Case IDs to reduce lookup overhead
- Use connection pooling for high-volume automation frameworks

## Real-World Examples

### Example 1: Healthcare Compliance Scenario

**Context**: Regulated healthcare environment requiring comprehensive audit trail for all system requirements.

**Implementation**: Established traceability pattern linking all requirements to test cases. When defects are logged, they are linked to failed test cases and originating requirements.

```python
# Minimal pattern: Requirement linking during test case creation
# In Kualitee interface: Link Test Case TC-001 to Requirement REQ-001
# When defect logged: Link Defect DEF-001 to TC-001 and REQ-001

# API pattern for status update after test execution
def update_test_status(test_case_id, status):
    payload = {
        "project_id": os.getenv("KUALITEE_PROJECT_ID"),
        "test_case_id": test_case_id,
        "status": status,  # 1=Passed, 2=Failed
        "token": os.getenv("KUALITEE_API_TOKEN")
    }
    requests.post(
        "https://apiss.kualitee.com/api/v2/test_case_execution/change_status",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
```

**Key Takeaway**: Traceability pattern generates verifiable audit trail automatically. Healthcare customer achieved 44% testing speed increase by eliminating manual tracking overhead.

### Example 2: CI/CD Integration Scenario

**Context**: CircleCI pipeline requiring real-time quality gates based on test execution results.

**Implementation**: Integrated Kualitee API status updates in test automation framework. Pipeline fails build immediately if critical tests report 'Failed'.

```python
# Minimal pattern: Status update in test teardown
def teardown_test(test_case_id, test_passed):
    status = 1 if test_passed else 2
    update_kualitee_status(
        project_id=os.getenv("KUALITEE_PROJECT_ID"),
        test_case_id=test_case_id,
        execution_status=status,
        api_token=os.getenv("KUALITEE_API_TOKEN")
    )

# CircleCI config.yml integration
# - run: pytest --kualitee-sync
#   environment:
#     KUALITEE_PROJECT_ID: "12345"
#     KUALITEE_API_TOKEN: ${{ secrets.KUALITEE_TOKEN }}
```

**Key Takeaway**: Real-time API synchronization transforms Kualitee into instantaneous quality gate. Enables continuous delivery with immediate feedback on test failures.

## Related Resources

For extensive reference materials, see:
- `templates/`: Reusable code templates for API integration
- Kualitee API documentation: https://apiss.kualitee.com/api/v2/
- Test Lab interface for parameter extraction

## Notes

- Kualitee supports both Cloud and On-Premise deployments. Confirm deployment option for enterprise requirements.
- AI features (Hootie) are most effective for simple test case generation. Complex validation requires human expertise.
- Build/Module segmentation is critical for multi-platform projects. Avoid using Test Scenarios for platform differentiation.
- Active reporting configuration is essential for proactive quality management. Default reports provide limited visibility.

