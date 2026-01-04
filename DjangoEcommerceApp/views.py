from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
<<<<<<< Updated upstream
from .services.stock_service import get_cart_stock_status
=======
from django.shortcuts import redirect
from .models import Cart, Products, CustomerUser
>>>>>>> Stashed changes

# Create your views here.
def add_to_cart(request, product_id):
    """
    Add a product to cart, respecting stock availability.
    """
    product = Products.objects.get(id=product_id)

    # Determine customer for the current request
    from .models import CustomUser
    customer_user = request.user if request.user.is_authenticated else CustomUser.objects.first()

    try:
        customer = CustomerUser.objects.get(auth_user_id=customer_user)
    except CustomerUser.DoesNotExist:
        # Fallback for test cases
        customer = CustomerUser.objects.first()

    # Always allow adding to cart, even for out-of-stock items
    # Set quantity to 0 if out of stock, otherwise limit to available stock
    quantity = 0 if product.in_stock_total == 0 else min(int(request.POST.get('quantity', 1)), product.in_stock_total)

    # Create or update cart item
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Adjust quantity, allowing 0 for out-of-stock items
        cart_item.quantity = 0 if product.in_stock_total == 0 else min(cart_item.quantity + quantity, product.in_stock_total)
        cart_item.save()

    if product.in_stock:
        messages.success(request, 'Product added to cart successfully!')
    else:
        messages.warning(request, 'Product is out of stock! Adding to cart but checkout will be limited.')

    return redirect('cart_view')

def cart_view(request):
    """
    Display cart with stock status, with enhanced handling of out-of-stock items.
    """
    # TODO: Replace with actual customer authentication
    from .models import CustomUser
    customer_user = request.user if request.user.is_authenticated else CustomUser.objects.first()

    try:
        customer = CustomerUser.objects.get(auth_user_id=customer_user)
    except CustomerUser.DoesNotExist:
        # Fallback for test cases
        customer = CustomerUser.objects.first()

    # Fetch cart items and annotate with stock status
    cart_items = Cart.objects.filter(customer=customer).select_related('product')

    # Track out of stock items with more comprehensive checks
    out_of_stock_items = []
    for item in cart_items:
        # If product is not in stock or requested quantity exceeds available stock
        if (not item.product.in_stock or
            item.quantity > item.product.in_stock_total):
            out_of_stock_items.append(item)

    # Keep out-of-stock items in the cart, but mark them
    # Refresh cart_items to reflect current status
    cart_items = Cart.objects.filter(customer=customer).select_related('product')

    return render(request, 'cart.html', {
        'cart_items': cart_items if cart_items.exists() else [],
        'out_of_stock_items': out_of_stock_items,
        'can_checkout': len(out_of_stock_items) == 0
    })

def update_cart_quantity(request, cart_item_id):
    """
    Update cart item quantity respecting stock limits.
    Prevents quantity changes for out-of-stock or limited stock items.
    """
    cart_item = Cart.objects.get(id=cart_item_id)

    # Check if product is out of stock or has insufficient stock
    if not cart_item.product.in_stock or cart_item.product.in_stock_total == 0:
        messages.warning(request, f'{cart_item.product.product_name} is out of stock. Cannot update quantity.')
        return redirect('cart_view')

    # Get requested quantity
    new_quantity = int(request.POST.get('quantity', 1))

    # Prevent quantity increase beyond available stock
    if new_quantity > cart_item.product.in_stock_total:
        messages.warning(request, f'Maximum available quantity for {cart_item.product.product_name} is {cart_item.product.in_stock_total}.')
        cart_item.quantity = cart_item.product.in_stock_total
    else:
        cart_item.quantity = new_quantity

    cart_item.save()

    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    """
    Remove an item from the cart.
    """
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()

    messages.success(request, 'Item removed from cart!')
    return redirect('cart_view')
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