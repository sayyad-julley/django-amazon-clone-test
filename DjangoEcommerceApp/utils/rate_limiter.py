import time
import functools
from typing import Callable, Any
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
import ipaddress
import logging

# Configure logging
logger = logging.getLogger('rate_limiter')
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('rate_limit.log')
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class RateLimiterException(Exception):
    """Custom exception for rate limiting violations."""
    pass

def get_client_ip(request: HttpRequest) -> str:
    """
    Robust method to get client IP address with multiple fallback mechanisms.

    Priority order:
    1. X-Forwarded-For (proxy)
    2. HTTP_X_REAL_IP (Nginx)
    3. REMOTE_ADDR (fallback)

    Handles IPv4 and IPv6 normalization.
    """
    # Try X-Forwarded-For (could be comma-separated list)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Try X-Real-IP
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        ip = x_real_ip if x_real_ip else request.META.get('REMOTE_ADDR')

    try:
        # Normalize IP address
        return str(ipaddress.ip_address(ip))
    except ValueError:
        # If IP is invalid, use a default marker
        return 'unknown_ip'

def enhanced_rate_limit(
    max_requests: int = 10,
    window_seconds: int = 60,
    key_prefix: str = 'rate_limit',
    error_message: str = 'Too many requests. Please try again later.',
    progressive_delay: bool = False
) -> Callable:
    """
    Enhanced rate limiting decorator with configurable parameters.

    Args:
        max_requests (int): Maximum number of requests allowed in the window.
        window_seconds (int): Time window in seconds.
        key_prefix (str): Prefix for cache key to allow different limit groups.
        error_message (str): Custom error message for rate limit violation.
        progressive_delay (bool): Enable progressive delays for repeated violations.

    Returns:
        Decorator function for rate limiting.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
            # Get client IP
            client_ip = get_client_ip(request)

            # Create a unique cache key
            cache_key = f'{key_prefix}_{client_ip}'
            violation_cache_key = f'{cache_key}_violations'

            # Get current timestamp and request timestamps from cache
            current_time = time.time()
            request_timestamps = cache.get(cache_key, [])

            # Remove timestamps outside the current window
            request_timestamps = [
                ts for ts in request_timestamps
                if current_time - ts <= window_seconds
            ]

            # Check if rate limit is exceeded
            if len(request_timestamps) >= max_requests:
                # Get the oldest timestamp in the current window
                oldest_request_time = request_timestamps[0]
                retry_after = int(window_seconds - (current_time - oldest_request_time))

                # Implement progressive delay if enabled
                if progressive_delay:
                    # Increase delay exponentially after repeated violations
                    violation_count = cache.get(violation_cache_key, 0)
                    retry_after *= (violation_count + 1)
                    cache.set(violation_cache_key, violation_count + 1, window_seconds)

                # Log rate limit violation
                logger.warning(
                    f"Rate limit violation - IP: {client_ip}, "
                    f"Max Requests: {max_requests}, "
                    f"Window: {window_seconds}s, "
                    f"Violations: {violation_count if progressive_delay else 'N/A'}"
                )

                # Create a detailed rate limit response
                response = HttpResponse(error_message, status=429)
                response['Retry-After'] = str(max(1, retry_after))
                response['X-RateLimit-Limit'] = str(max_requests)
                response['X-RateLimit-Remaining'] = '0'
                response['X-RateLimit-Reset'] = str(int(oldest_request_time + window_seconds))

                return response

            # Add current request timestamp
            request_timestamps.append(current_time)

            # Store updated timestamps
            cache.set(cache_key, request_timestamps, window_seconds)

            # Log successful request
            logger.info(
                f"Rate limit check passed - IP: {client_ip}, "
                f"Requests: {len(request_timestamps)}/{max_requests}, "
                f"Window: {window_seconds}s"
            )

            # Execute the original function
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

# Predefined rate limit configurations
def strict_auth_rate_limit(func: Callable) -> Callable:
    """
    Strict rate limiting for authentication endpoints.
    5 requests per minute with progressive delay.
    """
    return enhanced_rate_limit(
        max_requests=5,
        window_seconds=60,
        key_prefix='strict_auth',
        error_message='Authentication requests are temporarily limited. Please wait and try again.',
        progressive_delay=True
    )(func)

def standard_api_rate_limit(func: Callable) -> Callable:
    """
    Standard rate limiting for general API endpoints.
    10 requests per minute.
    """
    return enhanced_rate_limit(
        max_requests=10,
        window_seconds=60,
        key_prefix='standard_api',
        error_message='Too many requests. Please slow down.'
    )(func)

def rest_auth_rate_limit(func: Callable) -> Callable:
    """
    Enhanced rate limiting for REST API authentication endpoints.
    Implements adaptive rate limiting with more granular controls:
    - 5 requests per minute for login
    - Progressive delay with exponential backoff
    - Different limits for login, registration, and password reset
    - Supports per-user and per-IP tracking
    """
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        # Determine the authentication action for more specific rate limiting
        auth_action = request.path.split('/')[-1]

        # Configure limits based on the authentication action
        action_limits = {
            'login': {
                'max_requests': 5,
                'window_seconds': 60,
                'key_prefix': 'login_auth_api',
                'error_message': 'Too many login attempts. Please wait and retry.',
                'progressive_delay': True
            },
            'register': {
                'max_requests': 3,
                'window_seconds': 300,  # 5 minutes for registration
                'key_prefix': 'register_auth_api',
                'error_message': 'Registration temporarily limited. Please try again later.',
                'progressive_delay': True
            },
            'reset-password': {
                'max_requests': 2,
                'window_seconds': 3600,  # 1 hour for password reset
                'key_prefix': 'reset_password_api',
                'error_message': 'Password reset attempts exceeded. Please contact support.',
                'progressive_delay': True
            },
            'default': {
                'max_requests': 5,
                'window_seconds': 60,
                'key_prefix': 'default_auth_api',
                'error_message': 'Authentication API rate limit exceeded. Please wait and retry.',
                'progressive_delay': True
            }
        }

        # Select appropriate limit configuration
        limit_config = action_limits.get(auth_action, action_limits['default'])

        # Use enhanced rate limiter with specific configuration
        return enhanced_rate_limit(
            max_requests=limit_config['max_requests'],
            window_seconds=limit_config['window_seconds'],
            key_prefix=limit_config['key_prefix'],
            error_message=limit_config['error_message'],
            progressive_delay=limit_config['progressive_delay']
        )(func)(request, *args, **kwargs)

    return wrapper

def user_profile_rate_limit(func: Callable) -> Callable:
    """
    Rate limiting for user profile and logout endpoints.
    10 requests per minute with moderate error handling.
    """
    return enhanced_rate_limit(
        max_requests=10,
        window_seconds=60,
        key_prefix='user_profile_api',
        error_message='User profile API rate limit exceeded. Please wait and retry.',
        progressive_delay=False
    )(func)