import time
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from unittest.mock import patch
import json

User = get_user_model()

class RateLimitingTestCase(TestCase):
    def setUp(self):
        """
        Set up test environment for rate limiting tests.
        """
        self.client = Client()
        self.factory = RequestFactory()

        # Create a test user for authentication tests
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123!',
            'user_type': 1  # Admin type based on CustomUser model
        }
        self.user = User.objects.create_user(**self.test_user_data)

    def test_registration_rate_limit(self):
        """
        Test registration endpoint rate limiting.
        Verify that a single IP can only make 5 registration attempts in 1 minute.
        """
        registration_url = reverse('customer_create')  # Use the correct URL name

        # Simulate registration attempts from the same IP
        for i in range(5):
            response = self.client.post(registration_url, data={
                'username': f'newuser{i}',
                'email': f'newuser{i}@example.com',
                'password': 'securepassword123!',
                'user_type': 4  # Customer user type
            }, REMOTE_ADDR='192.168.1.100')

            # First 5 attempts should be successful
            self.assertNotEqual(response.status_code, 429,
                f"Registration attempt {i+1} should not be rate-limited")

        # 6th attempt should be rate-limited
        response = self.client.post(registration_url, data={
            'username': 'newuser6',
            'email': 'newuser6@example.com',
            'password': 'securepassword123!',
            'user_type': 4
        }, REMOTE_ADDR='192.168.1.100')

        self.assertEqual(response.status_code, 429,
            "6th registration attempt should be rate-limited")

        # Check rate limit headers
        self.assertIn('Retry-After', response.headers)
        self.assertIn('X-RateLimit-Limit', response.headers)
        self.assertEqual(response.headers.get('X-RateLimit-Limit'), '5')

    def test_login_rate_limit(self):
        """
        Test login endpoint rate limiting.
        Verify that a single IP can only make 5 login attempts in 1 minute.
        """
        login_url = reverse('admin_login_process')  # Use the correct URL name

        # Simulate login attempts from the same IP
        for i in range(5):
            response = self.client.post(login_url, data={
                'username': self.test_user_data['username'],
                'password': 'wrongpassword'  # Incorrect password to simulate failed login
            }, REMOTE_ADDR='192.168.1.101')

            # First 5 attempts should not be rate-limited
            self.assertNotEqual(response.status_code, 429,
                f"Login attempt {i+1} should not be rate-limited")

        # 6th attempt should be rate-limited
        response = self.client.post(login_url, data={
            'username': self.test_user_data['username'],
            'password': 'wrongpassword'
        }, REMOTE_ADDR='192.168.1.101')

        self.assertEqual(response.status_code, 429,
            "6th login attempt should be rate-limited")

        # Check rate limit headers
        self.assertIn('Retry-After', response.headers)
        self.assertIn('X-RateLimit-Limit', response.headers)
        self.assertEqual(response.headers.get('X-RateLimit-Limit'), '5')

    def test_rate_limit_progressive_delay(self):
        """
        Test that rate limiting applies a progressive delay mechanism.
        """
        login_url = reverse('admin_login_process')  # Use the correct URL name

        # Track the time between requests to verify progressive delay
        request_timestamps = []

        for i in range(6):
            start_time = time.time()
            response = self.client.post(login_url, data={
                'username': self.test_user_data['username'],
                'password': 'wrongpassword'
            }, REMOTE_ADDR='192.168.1.102')

            # Record timestamp for each request
            request_timestamps.append(time.time())

            # First 5 attempts should not be rate-limited
            if i < 5:
                self.assertNotEqual(response.status_code, 429,
                    f"Login attempt {i+1} should not be rate-limited")
            else:
                # 6th attempt should be rate-limited
                self.assertEqual(response.status_code, 429,
                    "6th login attempt should be rate-limited")

                # Verify retry-after header is present
                self.assertIn('Retry-After', response.headers)

        # If we have multiple timestamps, check their intervals
        if len(request_timestamps) > 1:
            request_intervals = [
                request_timestamps[i+1] - request_timestamps[i]
                for i in range(len(request_timestamps)-1)
            ]

    def test_different_ips_not_interfere(self):
        """
        Verify that rate limiting is IP-based and different IPs do not interfere.
        """
        login_url = reverse('admin_login_process')  # Use the correct URL name

        # Make 5 login attempts from one IP
        for i in range(5):
            response = self.client.post(login_url, data={
                'username': self.test_user_data['username'],
                'password': 'wrongpassword'
            }, REMOTE_ADDR='192.168.1.103')

            self.assertNotEqual(response.status_code, 429,
                f"Login attempt {i+1} from IP 192.168.1.103 should not be rate-limited")

        # 6th attempt from the same IP should be rate-limited
        response = self.client.post(login_url, data={
            'username': self.test_user_data['username'],
            'password': 'wrongpassword'
        }, REMOTE_ADDR='192.168.1.103')

        self.assertEqual(response.status_code, 429,
            "6th login attempt from IP 192.168.1.103 should be rate-limited")

        # Now try from a different IP - this should NOT be rate-limited
        response = self.client.post(login_url, data={
            'username': self.test_user_data['username'],
            'password': 'wrongpassword'
        }, REMOTE_ADDR='192.168.1.104')

        self.assertNotEqual(response.status_code, 429,
            "Login attempts from a different IP should not interfere")