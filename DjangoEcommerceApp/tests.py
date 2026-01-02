from django.test import TestCase
from .models import Products, Cart, CartItem, CustomerUser, CustomUser, MerchantUser, SubCategories, Categories

class ProductStockValidationTestCase(TestCase):
    def setUp(self):
        # Create a test customer
        self.user, _ = CustomUser.objects.get_or_create(username='testuser', user_type=4)
        # Ensure only one CustomerUser exists for this user
        self.customer, _ = CustomerUser.objects.get_or_create(auth_user_id=self.user)

        # Create a test merchant
        # Create a merchant outside of the test's setup process
        merchant_user = CustomUser.objects.filter(user_type=3).first()
        if not merchant_user:
            from django.utils.crypto import get_random_string
            merchant_username = f'merchant_{get_random_string(8)}'
            merchant_user = CustomUser.objects.create(username=merchant_username, user_type=3)

        # Check if merchant user already has a merchant profile
        try:
            self.merchant = merchant_user.merchantuser
        except MerchantUser.DoesNotExist:
            self.merchant = MerchantUser.objects.create(
                auth_user_id=merchant_user,
                company_name='Test Merchant',
                gst_details='GSTIN123',
                address='Test Address'
            )

        # Create a product in stock
        self.in_stock_product = Products.objects.create(
            product_name='Test Product',
            is_in_stock=True,
            in_stock_total=10,
            url_slug='test-product',
            subcategories_id=SubCategories.objects.create(
                title='Test Subcategory',
                url_slug='test-subcategory',
                category_id=Categories.objects.create(title='Test Category', url_slug='test-category', thumbnail=None),
                thumbnail=None
            ),
            added_by_merchant=self.merchant,
            brand='Test Brand',
            product_max_price='100',
            product_discount_price='90',
            product_description='Test Description',
            product_long_description='Long Test Description'
        )

        # Create an out of stock product
        self.out_of_stock_product = Products.objects.create(
            product_name='Out of Stock Product',
            is_in_stock=False,
            in_stock_total=0,
            url_slug='out-of-stock-product',
            subcategories_id=self.in_stock_product.subcategories_id,
            added_by_merchant=self.merchant,
            brand='Test Brand',
            product_max_price='100',
            product_discount_price='90',
            product_description='Test Description',
            product_long_description='Long Test Description'
        )

    def test_stock_validation(self):
        # Test product in stock
        self.assertTrue(self.in_stock_product.validate_stock(5))

        # Test product out of stock
        self.assertFalse(self.out_of_stock_product.validate_stock(1))

        # Test product with insufficient stock
        self.assertFalse(self.in_stock_product.validate_stock(20))

    def test_cart_item_validation(self):
        # Create a cart
        cart = Cart.objects.create(customer=self.customer)

        # Add in-stock product
        cart_item_valid = CartItem.objects.create(
            cart=cart,
            product=self.in_stock_product,
            quantity=5
        )
        self.assertTrue(cart_item_valid.is_valid())

        # Add out-of-stock product
        cart_item_invalid = CartItem.objects.create(
            cart=cart,
            product=self.out_of_stock_product,
            quantity=1
        )
        self.assertFalse(cart_item_invalid.is_valid())
