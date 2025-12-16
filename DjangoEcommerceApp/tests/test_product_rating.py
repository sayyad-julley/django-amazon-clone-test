from django.test import TestCase
from django.contrib.auth import get_user_model
from DjangoEcommerceApp.models import Products, ProductReviews, CustomerUser, SubCategories, Categories, MerchantUser

class ProductRatingTestCase(TestCase):
    def setUp(self):
        # Create necessary related objects
        CustomUser = get_user_model()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

        self.category = Categories.objects.create(title='Test Category', url_slug='test-category', thumbnail=None, description='Test Description')
        self.subcategory = SubCategories.objects.create(category_id=self.category, title='Test Subcategory', url_slug='test-subcategory', thumbnail=None, description='Test Subcategory Description')

        merchant = MerchantUser.objects.create(auth_user_id=self.user, company_name='Test Merchant')
        self.customer = CustomerUser.objects.create(auth_user_id=self.user)

        self.product = Products.objects.create(
            url_slug='test-product',
            subcategories_id=self.subcategory,
            product_name='Test Product',
            brand='Test Brand',
            product_max_price='100',
            product_discount_price='90',
            product_description='Test Description',
            product_long_description='Long Description',
            added_by_merchant=merchant
        )

    def test_initial_rating(self):
        """Test that a product's initial rating is 0.0"""
        self.assertEqual(self.product.average_rating, 0.0)
        self.assertEqual(self.product.dynamic_average_rating, 0.0)

    def test_single_review_rating(self):
        """Test average rating with a single review"""
        review = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=4.5,
            review_image=None,
            review='Great product'
        )

        # Reload the product to get updated rating
        self.product.refresh_from_db()

        self.assertEqual(float(self.product.average_rating), 4.5)
        self.assertEqual(float(self.product.dynamic_average_rating), 4.5)

    def test_multiple_review_average(self):
        """Test average rating with multiple reviews"""
        reviews = [
            ProductReviews.objects.create(
                product_id=self.product,
                user_id=self.customer,
                rating=4.0,
                review_image=None,
                review='Good product'
            ),
            ProductReviews.objects.create(
                product_id=self.product,
                user_id=self.customer,
                rating=5.0,
                review_image=None,
                review='Excellent product'
            )
        ]

        # Reload the product to get updated rating
        self.product.refresh_from_db()

        self.assertEqual(float(self.product.average_rating), 4.5)
        self.assertEqual(float(self.product.dynamic_average_rating), 4.5)

    def test_review_deletion_impact(self):
        """Test how deleting a review affects the average rating"""
        reviews = [
            ProductReviews.objects.create(
                product_id=self.product,
                user_id=self.customer,
                rating=4.0,
                review_image=None,
                review='Good product'
            ),
            ProductReviews.objects.create(
                product_id=self.product,
                user_id=self.customer,
                rating=5.0,
                review_image=None,
                review='Excellent product'
            )
        ]

        # Reload the product to get updated rating
        self.product.refresh_from_db()
        self.assertEqual(float(self.product.average_rating), 4.5)

        # Delete one review
        reviews[0].delete()

        # Reload the product again
        self.product.refresh_from_db()
        self.assertEqual(float(self.product.average_rating), 5.0)

    def test_deactivated_review_not_counted(self):
        """Test that inactive reviews are not counted in average"""
        active_review = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=4.0,
            review_image=None,
            review='Good product',
            is_active=1
        )

        inactive_review = ProductReviews.objects.create(
            product_id=self.product,
            user_id=self.customer,
            rating=1.0,
            review_image=None,
            review='Bad product',
            is_active=0
        )

        # Reload the product to get updated rating
        self.product.refresh_from_db()

        # Only active review should count
        self.assertEqual(float(self.product.average_rating), 4.0)
        self.assertEqual(float(self.product.dynamic_average_rating), 4.0)
