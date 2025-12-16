from django.test import TestCase, RequestFactory
from django.core.cache import cache
from unittest.mock import patch
from ..utils.rate_limiter import enhanced_rate_limit, get_client_ip, RateLimiterException
from django.urls import reverse
import time

class RateLimiterTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Clear cache before each test
        cache.clear()

    def test_client_ip_detection(self):
        """Test IP detection mechanism"""
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'
        self.assertEqual(get_client_ip(request), '192.168.1.1')

        del request.META['HTTP_X_FORWARDED_FOR']
        request.META['HTTP_X_REAL_IP'] = '10.0.0.2'
        self.assertEqual(get_client_ip(request), '10.0.0.2')

        del request.META['HTTP_X_REAL_IP']
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.assertEqual(get_client_ip(request), '127.0.0.1')

    def test_rate_limiting_basic(self):
        """Test basic rate limiting functionality"""
        @enhanced_rate_limit(max_requests=2, window_seconds=60)
        def mock_view(request):
            return "Success"

        request1 = self.factory.get('/')
        request2 = self.factory.get('/')
        request3 = self.factory.get('/')

        # First two requests should succeed
        self.assertEqual(mock_view(request1), "Success")
        self.assertEqual(mock_view(request2), "Success")

        # Third request should be rate limited
        response = mock_view(request3)
        self.assertEqual(response.status_code, 429)
        self.assertIn('Retry-After', response)
        self.assertIn('X-RateLimit-Limit', response)
        self.assertIn('X-RateLimit-Remaining', response)
        self.assertIn('X-RateLimit-Reset', response)

    def test_rate_limiting_window(self):
        """Test rate limiting with time window"""
        @enhanced_rate_limit(max_requests=2, window_seconds=1)
        def mock_view(request):
            return "Success"

        request1 = self.factory.get('/')
        request2 = self.factory.get('/')
        request3 = self.factory.get('/')

        # First two requests should succeed
        self.assertEqual(mock_view(request1), "Success")
        self.assertEqual(mock_view(request2), "Success")

        # Wait for window to expire
        time.sleep(1.1)

        # Third request after window should succeed
        self.assertEqual(mock_view(request3), "Success")

    def test_progressive_delay(self):
        """Test progressive delay for repeated violations"""
        @enhanced_rate_limit(max_requests=1, window_seconds=60, progressive_delay=True)
        def mock_view(request):
            return "Success"

        request = self.factory.get('/')

        # First request should succeed
        self.assertEqual(mock_view(request), "Success")

        # Subsequent requests should be rate limited with increasing delay
        response1 = mock_view(request)
        self.assertEqual(response1.status_code, 429)
        retry_after1 = int(response1['Retry-After'])

        # Simulate another violation
        response2 = mock_view(request)
        retry_after2 = int(response2['Retry-After'])

        self.assertGreater(retry_after2, retry_after1)