from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from .models import Cart, CartItem, Products, CustomerUser

# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request, "demo.html")

def adminLogin(request):
    return render(request, "admin_templates/signin.html")

def adminLoginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def adminLogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))

def checkout_process(request):
    try:
        # Assuming the customer is logged in and we can retrieve their cart
        customer_user = CustomerUser.objects.get(auth_user_id=request.user)
        cart = Cart.objects.get(customer=customer_user)

        # Get detailed stock validation information
        out_of_stock_details = []
        for item in cart.items.all():
            if not item.is_valid():
                out_of_stock_details.append({
                    'product_name': item.product.product_name,
                    'current_stock': item.product.in_stock_total,
                    'requested_quantity': item.quantity
                })

        # If any out-of-stock items, provide detailed guidance
        if out_of_stock_details:
            detailed_warning = "The following items are unavailable or have insufficient stock:\n"
            for detail in out_of_stock_details:
                detailed_warning += (
                    f"- {detail['product_name']}: "
                    f"Requested {detail['requested_quantity']}, "
                    f"Available {detail['current_stock']}\n"
                )
            detailed_warning += "Please adjust your cart quantities or remove these items."
            messages.warning(request, detailed_warning)

        # Automatically remove out-of-stock items
        out_of_stock_items = cart.remove_out_of_stock_items()

        # Check if cart is now empty after removing out-of-stock items
        if not cart.items.exists():
            messages.error(request, "Your cart is now empty due to out-of-stock items. Please add available products.")
            return HttpResponseRedirect(reverse('cart_view'))

        # Validate remaining cart items
        if not cart.validate_cart_items():
            messages.error(request, "Some items in your cart have become unavailable. Please review your cart.")
            return HttpResponseRedirect(reverse('cart_view'))

        # If all items are valid, proceed with checkout
        # Add your checkout logic here
        return HttpResponseRedirect(reverse('checkout_success'))

    except CustomerUser.DoesNotExist:
        messages.error(request, "Please log in to proceed with checkout.")
        return HttpResponseRedirect(reverse('login'))
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return HttpResponseRedirect(reverse('cart_view'))