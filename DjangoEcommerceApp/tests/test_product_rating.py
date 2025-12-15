from django.test import TestCase
from django.contrib.auth import get_user_model
from DjangoEcommerceApp.models import Products, ProductReviews, CustomerUser, Categories, SubCategories, MerchantUser

class ProductRatingTestCase(TestCase):
    def setUp(self):
        # Create test user and merchant
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.merchant = MerchantUser.objects.create(
            auth_user_id=self.user,
            company_name='Test Company',
            gst_details='123456',
            address='Test Address'
        )

        # Create test category and subcategory
        self.category = Categories.objects.create(
            title='Test Category',
            url_slug='test-category',
            description='Test Description'
        )
        self.subcategory = SubCategories.objects.create(
            category_id=self.category,
            title='Test Subcategory',
            url_slug='test-subcategory'
        )

        # Create test product
        self.product = Products.objects.create(
            subcategories_id=self.subcategory,
            product_name='Test Product',
            brand='Test Brand',
            product_max_price='100',
            product_discount_price='80',
            product_description='Test Description',
            added_by_merchant=self.merchant
        )

        # Create test customer
        self.customer = CustomerUser.objects.create(auth_user_id=self.user)

    def create_review(self, rating):
        return ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=float(rating)
        )

    def test_no_reviews_rating(self):
        """Test that product with no reviews has zero rating"""
        self.assertEqual(self.product.dynamic_average_rating, 0.0)
        self.assertEqual(self.product.average_rating, 0.0)

    def test_single_review_rating(self):
        """Test rating calculation with a single review"""
        self.create_review(4.5)
        self.assertEqual(self.product.dynamic_average_rating, 4.5)
        self.assertEqual(self.product.average_rating, 4.5)

    def test_multiple_reviews_rating(self):
        """Test rating calculation with multiple reviews"""
        self.create_review(4)
        self.create_review(5)
        self.create_review(3)
        self.assertEqual(self.product.dynamic_average_rating, 4.0)
        self.assertEqual(self.product.average_rating, 4.0)

    def test_review_deletion_impacts_rating(self):
        """Test that deleting a review updates the product rating"""
        review1 = self.create_review(4)
        review2 = self.create_review(5)

        # Initial rating check
        self.assertEqual(self.product.dynamic_average_rating, 4.5)

        # Delete one review
        review1.delete()
        self.assertEqual(self.product.dynamic_average_rating, 5.0)

        # Delete last review
        review2.delete()
        self.assertEqual(self.product.dynamic_average_rating, 0.0)
