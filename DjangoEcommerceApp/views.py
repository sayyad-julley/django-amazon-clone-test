from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from .models import CustomUser, CustomerUser

# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request,"demo.html")

def adminLogin(request):
    return render(request,"admin_templates/signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request,user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))


def login_user_view(request):
    if request.method != "POST":
        return render(request, "login.html")
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect based on user type if needed, or just home
        return HttpResponseRedirect("/")
    else:
        messages.error(request, "Invalid Login Details")
        return HttpResponseRedirect(reverse("login"))

def register_user_view(request):
    if request.method != "POST":
        return render(request, "register.html")
        
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=4)
        user.save()
        messages.success(request, "Registration Successful")
        return HttpResponseRedirect(reverse("login"))
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return HttpResponseRedirect(reverse("register"))

def logout_user_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def password_reset_request(request):
    if request.method != "POST":
        return render(request, "password_reset.html")
    
    email = request.POST.get("email")
    # Simulation of password reset email
    messages.success(request, f"Password reset email sent to {email}")
    return HttpResponseRedirect(reverse("login"))

# Simple in-memory rate limiter for demonstration
RATE_LIMIT_STORE = {}

@csrf_exempt
def api_login_view(request):
    ip = request.META.get('REMOTE_ADDR')
    current_time = time.time()
    
    # Rate Limiting Logic: Max 3 requests per 60 seconds
    if ip in RATE_LIMIT_STORE:
        last_requests = [t for t in RATE_LIMIT_STORE[ip] if current_time - t < 60]
        RATE_LIMIT_STORE[ip] = last_requests
        if len(last_requests) >= 3:
            response = JsonResponse({"error": "Rate limit exceeded"}, status=429)
            response['Retry-After'] = '60'
            return response
    else:
        RATE_LIMIT_STORE[ip] = []
        
    RATE_LIMIT_STORE[ip].append(current_time)

    if request.method == "POST":
        try:
            data = request.POST
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                return JsonResponse({"message": "Login successful", "token": "dummy-token"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))