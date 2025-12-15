from django.test import TestCase
from django.contrib.auth import get_user_model
from DjangoEcommerceApp.models import Products, SubCategories, CustomerUser, ProductReviews, MerchantUser, Categories

class ProductRatingTestCase(TestCase):
    def setUp(self):
        # Create test data
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='12345')
        merchant = MerchantUser.objects.create(auth_user_id=user)

        category = Categories.objects.create(title='Test Category', url_slug='test-category', thumbnail='', description='')
        subcategory = SubCategories.objects.create(category_id=category, title='Test Subcategory', url_slug='test-subcategory', thumbnail='', description='')

        customer_user = CustomerUser.objects.create(auth_user_id=user)

        self.product = Products.objects.create(
            url_slug='test-product',
            subcategories_id=subcategory,
            product_name='Test Product',
            brand='Test Brand',
            product_max_price='100',
            product_discount_price='90',
            product_description='Test Description',
            product_long_description='Long Description',
            added_by_merchant=merchant
        )

    def test_dynamic_average_rating_empty(self):
        """Test that product with no reviews has 0.0 rating"""
        self.assertEqual(self.product.dynamic_average_rating, 0.0)

    def test_dynamic_average_rating_calculation(self):
        """Test dynamic average rating calculation"""
        # Add reviews
        ProductReviews.objects.create(
            product_id=self.product,
            user_id=CustomerUser.objects.first(),
            rating='4',
            review='Good product'
        )
        ProductReviews.objects.create(
            product_id=self.product,
            user_id=CustomerUser.objects.first(),
            rating='5',
            review='Great product'
        )

        # Reload the product to ensure fresh calculation
        product = Products.objects.get(id=self.product.id)
        self.assertEqual(product.dynamic_average_rating, 4.5)

    def test_dynamic_average_rating_inactive_reviews(self):
        """Test that inactive reviews do not affect rating"""
        # Add an active and an inactive review
        ProductReviews.objects.create(
            product_id=self.product,
            user_id=CustomerUser.objects.first(),
            rating='4',
            review='Good product',
            is_active=1
        )
        ProductReviews.objects.create(
            product_id=self.product,
            user_id=CustomerUser.objects.first(),
            rating='5',
            review='Great product',
            is_active=0  # Inactive review
        )

        # Reload the product to ensure fresh calculation
        product = Products.objects.get(id=self.product.id)
        self.assertEqual(product.dynamic_average_rating, 4.0)