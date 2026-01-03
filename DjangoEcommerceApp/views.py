from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from .services.stock_service import get_cart_stock_status

# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def cart_view(request):
    # Fetch cart items (implementation depends on your cart logic)
    cart_items = []  # Replace with actual cart item retrieval

    # Check stock status for cart items
    is_cart_in_stock = get_cart_stock_status(cart_items)

    context = {
        'cart_items': cart_items,
        'is_cart_in_stock': is_cart_in_stock
    }
    return render(request, 'cart.html', context)

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

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))