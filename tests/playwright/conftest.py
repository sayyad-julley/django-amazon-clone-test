"""
Playwright-Kualitee Integration Configuration
Implements the Push Model for real-time test result reporting
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import Any
from playwright.sync_api import Page

# Smart path resolution: Find framework root whether running from framework or injected repo
def find_framework_root():
    """Find the sdlc-agent-framework root directory."""
    current = Path(__file__).resolve().parent
    
    # Strategy 1: Check if we're in the framework (has src/mcp_servers/kualitee_server.py)
    for _ in range(5):  # Walk up max 5 levels
        framework_root = current
        kualitee_path = framework_root / "src" / "mcp_servers" / "kualitee_server.py"
        if kualitee_path.exists():
            return str(framework_root)
        if current.parent == current:  # Reached filesystem root
            break
        current = current.parent
    
    # Strategy 2: If injected, look for framework in common locations
    # When injected into repos/django-amazon-clone-test/tests/playwright/
    # Framework should be at ../../sdlc-agent-framework
    injected_path = Path(__file__).resolve().parent
    if "repos" in str(injected_path):
        # We're in a repos/*/tests/playwright structure
        repos_dir = injected_path
        while repos_dir.name != "repos" and repos_dir.parent != repos_dir:
            repos_dir = repos_dir.parent
        if repos_dir.name == "repos":
            framework_candidate = repos_dir.parent / "sdlc-agent-framework"
            if (framework_candidate / "src" / "mcp_servers" / "kualitee_server.py").exists():
                return str(framework_candidate)
    
    # Fallback: Use environment variable if set
    env_framework = os.getenv("SDLC_FRAMEWORK_ROOT")
    if env_framework and Path(env_framework).exists():
        return env_framework
    
    # Last resort: raise error with helpful message
    raise ImportError(
        f"Could not find sdlc-agent-framework root. "
        f"Tried: {Path(__file__).resolve().parent} and parent directories. "
        f"Set SDLC_FRAMEWORK_ROOT environment variable to framework root path."
    )

# Add framework root to Python path
framework_root = find_framework_root()
sys.path.insert(0, framework_root)

from src.mcp_servers.kualitee_server import KualiteeMCPServer


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "kualitee_id(id): mark test to sync with Kualitee test case ID"
    )


@pytest.fixture(scope="session")
def kualitee_server():
    """Initialize Kualitee server for test reporting"""
    return KualiteeMCPServer()


def pytest_runtest_makereport(item, call):
    """
    Hook that fires after each test to report results to Kualitee
    Implements the Push Model pattern from the integration documentation
    """
    if call.when == "call":  # Only run after test execution, not setup/teardown

        # Check if test has Kualitee ID marker
        kualitee_marker = item.get_closest_marker("kualitee_id")
        if not kualitee_marker:
            return  # Skip tests without Kualitee mapping

        # Extract test case ID and determine result
        test_case_id = kualitee_marker.args[0]
        status = "Passed" if call.excinfo is None else "Failed"

        # Build evidence from test info
        evidence = f"Automated Playwright test: {item.nodeid}"
        if call.excinfo:
            evidence += f" | Error: {str(call.excinfo.value)}"

        # Report to Kualitee (async call in sync context)
        try:
            # Get or create event loop for async operation
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context, create a task
                asyncio.create_task(_report_to_kualitee(test_case_id, status, evidence))
            else:
                # Run in sync context
                loop.run_until_complete(_report_to_kualitee(test_case_id, status, evidence))
        except Exception as e:
            print(f"⚠️  Failed to report to Kualitee: {e}")


async def _report_to_kualitee(test_case_id: str, status: str, evidence: str):
    """Async helper to report test results to Kualitee"""
    try:
        server = KualiteeMCPServer()
        result = await server.report_execution(
            project_id="20317",  # Django Amazon Clone project
            issue_key=test_case_id,
            status=status,
            evidence=evidence
        )

        if result.get("success"):
            print(f"✅ [Kualitee] Reported {status} for {test_case_id}")
        else:
            print(f"❌ [Kualitee] Failed to report {test_case_id}: {result.get('error')}")

    except Exception as e:
        print(f"❌ [Kualitee] Exception reporting {test_case_id}: {e}")


@pytest.fixture
def page(page: Page):
    """Enhanced page fixture with common setup"""
    # Set viewport and timeout defaults
    page.set_viewport_size({"width": 1280, "height": 720})
    page.set_default_timeout(10000)  # 10 second timeout

    yield page

    # Cleanup after test
    try:
        page.close()
    except:
        pass  # Page might already be closed