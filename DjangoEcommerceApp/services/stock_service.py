from DjangoEcommerceApp.models import Products, CustomerOrders

def validate_product_stock(product):
    """
    Validate the stock status of a product.

    Args:
        product (Products): The product to validate stock for

    Returns:
        bool: True if the product is in stock, False otherwise
    """
    if product.in_stock_total <= 0:
        product.in_stock = False
        product.save()
    return product.in_stock

def update_order_stock_status(order):
    """
    Update the stock status of an order based on product availability.

    Args:
        order (CustomerOrders): The order to update

    Returns:
        bool: True if order is in stock, False otherwise
    """
    order.is_in_stock = validate_product_stock(order.product_id)
    order.save()
    return order.is_in_stock

def get_cart_stock_status(cart_items):
    """
    Check the stock status for a list of cart items.

    Args:
        cart_items (list): List of cart items to check

    Returns:
        bool: True if all items are in stock, False otherwise
    """
    return all(validate_product_stock(item.product_id) for item in cart_items)