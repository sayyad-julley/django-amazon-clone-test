from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

import json
import time

# Rate limiting
_login_attempts = {}
RATE_LIMIT_WINDOW = 60  # seconds
MAX_LOGIN_ATTEMPTS = 5

def home_view(request):
    """Simple home page view."""
    return render(request, 'home.html')

def check_rate_limit(request):
    """Check and enforce rate limiting for login attempts."""
    client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    current_time = time.time()

    # Clean up old attempts
    _login_attempts[client_ip] = [
        attempt_time for attempt_time in _login_attempts.get(client_ip, [])
        if current_time - attempt_time < RATE_LIMIT_WINDOW
    ]

    remaining_attempts = MAX_LOGIN_ATTEMPTS - len(_login_attempts.get(client_ip, []))

    if remaining_attempts <= 0:
        # Return details about rate limit for retry-after
        return {
            'allowed': False,
            'retry_after': RATE_LIMIT_WINDOW
        }

    return {
        'allowed': True,
        'remaining_attempts': remaining_attempts
    }

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login for both customer and admin."""
    if request.method == 'GET':
        return render(request, 'auth/login.html')

    # Check rate limit
    rate_limit_result = check_rate_limit(request)

    # If not allowed, return 429 with retry-after header
    if not rate_limit_result['allowed']:
        # Add current attempt even if rate limited
        client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        _login_attempts.setdefault(client_ip, []).append(time.time())

        # Return rate limit response
        return JsonResponse({
            'error': 'Too many login attempts',
            'retry_after': rate_limit_result['retry_after']
        }, status=429)

    username = request.POST.get('username')
    password = request.POST.get('password')

    # Add current attempt to rate limit tracking
    _login_attempts.setdefault(request.META.get('REMOTE_ADDR', '0.0.0.0'), []).append(time.time())

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')  # Replace with your home page URL
    else:
        messages.error(request, 'Invalid username or password')
        return render(request, 'auth/login.html', status=401)

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration."""
    if request.method == 'GET':
        return render(request, 'auth/register.html')

    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate email
        validate_email(email)

        # Check password match
        if password1 != password2:
            raise ValidationError("Passwords do not match")

        # Validate password strength
        validate_password(password1)

        # Use Django's user model (which is CustomUser in this project)
        User = get_user_model()

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Optional: Set user type or do additional setup
        user.user_type = '4'  # Customer type
        user.save()

        login(request, user)
        return redirect('home')  # Replace with your home page URL

    except ValidationError as e:
        messages.error(request, str(e))
        return render(request, 'auth/register.html', status=400)

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login')  # Or any other desired redirect

@csrf_exempt
def api_login_view(request):
    """API endpoint for login with rate limiting."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        # Parse JSON payload
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Check rate limit
        rate_limit_result = check_rate_limit(request)

        # If not allowed, return 429 with retry-after header
        if not rate_limit_result['allowed']:
            # Add current attempt even if rate limited
            client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            _login_attempts.setdefault(client_ip, []).append(time.time())

            # Return rate limit response
            return JsonResponse({
                'error': 'Too many login attempts',
                'retry_after': rate_limit_result['retry_after']
            }, status=429)

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Logged in successfully'})
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)