import functools
import logging
import time
from typing import Callable, Any

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

def sliding_window_rate_limit(
    limit: int = 10,  # Number of requests allowed
    window: int = 60,  # Window size in seconds
    key_prefix: str = 'rate_limit'
) -> Callable:
    """
    A decorator for rate limiting using a sliding window algorithm.

    :param limit: Maximum number of requests allowed in the window
    :param window: Time window in seconds
    :param key_prefix: Prefix for the cache key
    :return: Decorator function
    """
    def decorator(view_func: Callable) -> Callable:
        @functools.wraps(view_func)
        def wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            # Generate a unique key based on client IP
            client_ip = _get_client_ip(request)
            cache_key = f'{key_prefix}:{client_ip}'

            # Get current timestamp
            current_time = int(time.time())

            # Retrieve or initialize the request log
            request_log = cache.get(cache_key, [])

            # Remove timestamps outside the current window
            request_log = [ts for ts in request_log if current_time - ts < window]

            # Check if rate limit is exceeded
            if len(request_log) >= limit:
                # Calculate time until the oldest request in the window expires
                retry_after = window - (current_time - request_log[0])

                logger.warning(
                    f'Rate limit exceeded for IP {client_ip}. '
                    f'Requests in window: {len(request_log)}, Retry after: {retry_after}s'
                )

                # Create response with 429 status and Retry-After header
                response = HttpResponse(
                    f'Too many requests. Try again in {retry_after} seconds.',
                    status=429
                )
                response['Retry-After'] = str(retry_after)
                return response

            # Add current timestamp to the request log
            request_log.append(current_time)

            # Store updated request log in cache with expiration
            cache.set(cache_key, request_log, timeout=window)

            # Call the original view
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator

def _get_client_ip(request: HttpRequest) -> str:
    """
    Get the client IP address, handling various proxy scenarios.

    :param request: HttpRequest object
    :return: Client IP address as a string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip
