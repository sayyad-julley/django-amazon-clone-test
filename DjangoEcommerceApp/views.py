from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from .utils.rate_limiter import strict_auth_rate_limit, rest_auth_rate_limit

# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request,"demo.html")

def adminLogin(request):
    return render(request,"admin_templates/signin.html")

@strict_auth_rate_limit  # 5 requests per minute with progressive delay
@rest_auth_rate_limit  # Adds an additional API-level rate limiting
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

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))