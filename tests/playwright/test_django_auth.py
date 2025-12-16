"""
Django Amazon Clone Authentication Tests
Implements Playwright-Kualitee integration using the Push Model

Each test is mapped to a Kualitee test case using the @pytest.mark.kualitee_id marker
Test results are automatically reported to Kualitee via the conftest.py hook
"""

import pytest
from playwright.sync_api import Page, expect


class TestAuthentication:
    """Authentication flow tests for Django Amazon Clone"""

    @pytest.mark.kualitee_id("1124940")
    def test_login_success(self, page: Page):
        """Test successful login with valid credentials"""
        # Navigate to login page
        page.goto("http://localhost:8000/auth/login/")

        # Verify login page loads
        expect(page.locator("h2")).to_contain_text("Login")

        # Fill login form
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "testpass123")

        # Submit form
        page.click("button[type='submit']")

        # Verify successful login (redirect or success message)
        expect(page).to_have_url("http://localhost:8000/")


    @pytest.mark.kualitee_id("1124941")
    def test_login_invalid_credentials(self, page: Page):
        """Test login failure with invalid credentials"""
        page.goto("http://localhost:8000/auth/login/")

        # Try invalid credentials
        page.fill("input[name='username']", "invaliduser")
        page.fill("input[name='password']", "wrongpassword")
        page.click("button[type='submit']")

        # Should stay on login page with error
        expect(page).to_have_url("http://localhost:8000/auth/login/")
        expect(page.locator(".alert, .error")).to_be_visible()


    @pytest.mark.kualitee_id("1124942")
    def test_logout_functionality(self, page: Page):
        """Test user logout functionality"""
        # First login
        page.goto("http://localhost:8000/auth/login/")
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "testpass123")
        page.click("button[type='submit']")

        # Verify logged in
        expect(page).to_have_url("http://localhost:8000/")

        # Logout
        page.click("a[href*='logout'], button:has-text('Logout')")

        # Verify logged out (redirected to login or homepage)
        expect(page.locator("a:has-text('Login'), h2:has-text('Login')")).to_be_visible()


class TestRegistration:
    """User registration tests"""

    @pytest.mark.kualitee_id("1124943")
    def test_user_registration(self, page: Page):
        """Test new user registration"""
        page.goto("http://localhost:8000/auth/register/")

        # Fill registration form
        page.fill("input[name='username']", f"newuser_{int(page.evaluate('Date.now()'))}")
        page.fill("input[name='email']", "newuser@example.com")
        page.fill("input[name='password1']", "securepassword123")
        page.fill("input[name='password2']", "securepassword123")

        # Submit registration
        page.click("button[type='submit']")

        # Verify registration success
        expect(page).to_have_url("http://localhost:8000/auth/login/")


class TestPasswordReset:
    """Password reset functionality tests"""

    @pytest.mark.kualitee_id("1124944")
    def test_password_reset_request(self, page: Page):
        """Test password reset request functionality"""
        page.goto("http://localhost:8000/auth/password-reset/")

        # Fill email for password reset
        page.fill("input[name='email']", "testuser@example.com")
        page.click("button[type='submit']")

        # Verify reset email sent confirmation
        expect(page.locator(".alert-success, .success")).to_contain_text("email")


class TestAPIRateLimit:
    """API Rate Limiting tests for AGENTIC-116"""

    @pytest.mark.kualitee_id("1124945")
    def test_api_rate_limit_enforcement(self, page: Page):
        """Test that API rate limiting returns 429 when exceeded"""

        # Test rapid API calls to trigger rate limit
        api_endpoint = "http://localhost:8000/api/auth/login/"

        # Make multiple rapid requests
        for i in range(5):
            response = page.request.post(api_endpoint, data={
                "username": "testuser",
                "password": "invalid"
            })

            if i >= 3:  # Expect rate limiting after several requests
                # Should get 429 or rate limit response
                assert response.status == 429 or "rate limit" in response.text().lower()


    @pytest.mark.kualitee_id("1124946")
    def test_rate_limit_retry_after_header(self, page: Page):
        """Test that rate limited responses include Retry-After header"""

        # Trigger rate limit
        api_endpoint = "http://localhost:8000/api/auth/login/"

        # Make requests until rate limited
        for i in range(10):
            response = page.request.post(api_endpoint, data={
                "username": "test",
                "password": "test"
            })

            if response.status == 429:
                # Verify Retry-After header is present
                headers = response.headers
                assert "retry-after" in [h.lower() for h in headers.keys()]
                break
        else:
            pytest.fail("Rate limit not triggered after 10 requests")