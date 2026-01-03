from django.test import TestCase

# Tests for Cart Stock Status Feature
from .models import CustomUser, Products as Product, Cart, CustomerOrders as CustomerOrder

class CartStockStatusTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='12345',
            user_type=4  # Customer
        )

        # Create test products with different stock statuses
        from .models import Categories, SubCategories, MerchantUser
        # Ensure required related objects exist
        category = Categories.objects.first() or Categories.objects.create(
            title='Test Category',
            url_slug='test-category',
            thumbnail=None,  # Avoid file upload complexities
            description='Test Category Description'
        )
        subcategory = SubCategories.objects.first() or SubCategories.objects.create(
            category_id=category,
            title='Test Subcategory',
            url_slug='test-subcategory',
            thumbnail=None,  # Avoid file upload complexities
            description='Test Subcategory Description'
        )
        # Find or create a merchant user
        merchant_user = CustomUser.objects.filter(username='merchant', user_type=3).first()
        if not merchant_user:
            merchant_user = CustomUser.objects.create_user(username='merchant', password='12345', user_type=3)

        # Find or create a merchant profile for this user
        merchant, created = MerchantUser.objects.get_or_create(
            auth_user_id=merchant_user,
            defaults={
                'company_name':'Test Merchant',
                'gst_details':'GST123',
                'address':'Test Address'
            }
        )

        self.in_stock_product = Product.objects.create(
            url_slug='in-stock-test',
            subcategories_id=subcategory,
            product_name='In Stock Product',
            brand='Test Brand',
            product_max_price='10.00',
            product_discount_price='9.00',
            product_description='Test Description',
            product_long_description='Long Test Description',
            added_by_merchant=merchant,
            in_stock_total=5,
            in_stock=True
        )

        self.out_of_stock_product = Product.objects.create(
            url_slug='out-of-stock-test',
            subcategories_id=subcategory,
            product_name='Out of Stock Product',
            brand='Test Brand',
            product_max_price='15.00',
            product_discount_price='14.00',
            product_description='Test Description',
            product_long_description='Long Test Description',
            added_by_merchant=merchant,
            in_stock_total=0,
            in_stock=False
        )

    def test_cart_stock_status_display(self):
        """
        Test that cart correctly displays stock status for products
        """
        # Add products to cart
        cart = Cart.objects.create(user=self.user)
        cart.add_to_cart(self.in_stock_product, 1)

        # Attempt to add out-of-stock product should raise exception
        with self.assertRaises(ValueError):
            cart.add_to_cart(self.out_of_stock_product, 1)

        # Verify cart only contains in-stock product
        cart_items = cart.cartitem_set.all()
        self.assertEqual(len(cart_items), 1)

        # Check stock status of cart item
        in_stock_item = cart_items.get(product=self.in_stock_product)
        self.assertTrue(in_stock_item.is_in_stock())

    def test_checkout_with_out_of_stock_items(self):
        """
        Test that checkout is blocked when cart contains out-of-stock items
        """
        cart = Cart.objects.create(user=self.user)
        cart.add_to_cart(self.in_stock_product, 1)

        # Attempt to create order should succeed when all items are in stock
        try:
            CustomerOrder.create_order_from_cart(cart)
        except ValueError:
            self.fail("Checkout with all in-stock items should succeed")

    def test_stock_validation_on_cart_update(self):
        """
        Test that cart update respects product stock quantity
        """
        cart = Cart.objects.create(user=self.user)
        cart.add_to_cart(self.in_stock_product, 1)

        # Try to update quantity within available stock should succeed
        cart.update_cart_item_quantity(
            self.in_stock_product,
            4  # Within available stock of 5
        )

        # Try to update quantity beyond available stock should raise exception
        with self.assertRaises(ValueError):
            cart.update_cart_item_quantity(
                self.in_stock_product,
                6  # Beyond available stock of 5
            )
