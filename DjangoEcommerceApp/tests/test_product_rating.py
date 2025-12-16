from django.test import TestCase
from DjangoEcommerceApp.models import CustomUser
from DjangoEcommerceApp.models import Products, ProductReviews, CustomerUser, Categories, SubCategories, MerchantUser
import uuid

class ProductRatingTestCase(TestCase):
    def setUp(self):
        # Generate unique usernames
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        merchant_username = f'merchant_{uuid.uuid4().hex[:8]}'

        # Create or get test data
        self.user, _ = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'password': '12345',
                'user_type': 4,
                'first_name': 'Test',
                'last_name': 'User'
            }
        )

        # Create or get merchant
        merchant_user, _ = CustomUser.objects.get_or_create(
            username=merchant_username,
            defaults={
                'password': '12345',
                'user_type': 3,
                'first_name': 'Test',
                'last_name': 'Merchant'
            }
        )

        # Create or get merchant profile
        self.merchant, _ = MerchantUser.objects.get_or_create(
            auth_user_id=merchant_user,
            defaults={'company_name': 'Test Company'}
        )

        # Create or get customer profile
        self.customer, _ = CustomerUser.objects.get_or_create(
            auth_user_id=self.user
        )

        # Create categories and subcategories
        self.category, _ = Categories.objects.get_or_create(
            title='Test Category',
            defaults={'url_slug': 'test-category'}
        )

        self.subcategory, _ = SubCategories.objects.get_or_create(
            category_id=self.category,
            title='Test Subcategory',
            defaults={'url_slug': 'test-subcategory'}
        )

        # Create product
        self.product, _ = Products.objects.get_or_create(
            product_name='Test Product',
            brand='Test Brand',
            subcategories_id=self.subcategory,
            added_by_merchant=self.merchant,
            defaults={'url_slug': 'test-product'}
        )

    def test_average_rating_calculation(self):
        # Test initial state
        self.assertEqual(self.product.dynamic_average_rating, 0.0)

        # Create reviews
        review1 = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=4.0,
            review_image=None
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 4.0)

        # Add another review
        review2 = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=5.0,
            review_image=None
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 4.5)

        # Delete a review
        review1.delete()

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 5.0)

        # Delete remaining review
        review2.delete()

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 0.0)

    def test_inactive_reviews(self):
        # Create review and mark as inactive
        review = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=4.0,
            review_image=None,
            is_active=0
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 0.0)

    def test_multiple_reviews_precision(self):
        # Test precision of rating calculation
        reviews_data = [
            (3.5, True),
            (4.0, True),
            (4.5, True),
            (2.0, False)  # Inactive review
        ]

        for rating, is_active in reviews_data:
            ProductReviews.objects.create(
                product_id=self.product,
                user_id=self.customer,
                rating=rating,
                review_image=None,
                is_active=1 if is_active else 0
            )

        self.product.refresh_from_db()
        self.assertEqual(self.product.dynamic_average_rating, 4.0)