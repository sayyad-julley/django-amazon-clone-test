from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Review

User = get_user_model()

class ProductRatingTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a product
        self.product = Product.objects.create(
            product_name='Test Product',
            brand='Test Brand',
            product_description='A test product description'
        )

    def test_initial_rating_is_none(self):
        """
        Test that a new product with no reviews has None as its rating
        """
        self.assertIsNone(self.product.average_rating)
        self.assertIsNone(self.product.calculated_average_rating)

    def test_add_single_review(self):
        """
        Test adding a single review updates the rating correctly
        """
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Good product'
        )

        # Refresh the product from the database
        self.product.refresh_from_db()

        # Check calculated and stored rating
        self.assertEqual(self.product.calculated_average_rating, 4)
        self.assertEqual(self.product.average_rating, 4)

    def test_multiple_reviews(self):
        """
        Test multiple reviews calculate average rating correctly
        """
        # Create multiple reviews
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4
        )

        # Create another user for a second review
        second_user = User.objects.create_user(
            username='seconduser',
            email='second@example.com',
            password='testpass456'
        )

        Review.objects.create(
            product=self.product,
            user=second_user,
            rating=5
        )

        # Refresh the product
        self.product.refresh_from_db()

        # Check calculated and stored rating
        self.assertEqual(self.product.calculated_average_rating, 4.5)
        self.assertEqual(self.product.average_rating, 4.5)

    def test_review_deletion(self):
        """
        Test that deleting a review updates the rating
        """
        review1 = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4
        )

        review2 = Review.objects.create(
            product=self.product,
            user=User.objects.create_user(
                username='deleteuser',
                email='delete@example.com',
                password='testpass789'
            ),
            rating=5
        )

        # Verify initial rating
        self.product.refresh_from_db()
        self.assertEqual(self.product.calculated_average_rating, 4.5)
        self.assertEqual(self.product.average_rating, 4.5)

        # Delete a review
        review1.delete()

        # Refresh and check new rating
        self.product.refresh_from_db()
        self.assertEqual(self.product.calculated_average_rating, 5)
        self.assertEqual(self.product.average_rating, 5)

    def test_product_without_reviews(self):
        """
        Verify behavior of a product with no reviews
        """
        no_review_product = Product.objects.create(
            product_name='No Review Product',
            brand='Test Brand'
        )

        self.assertIsNone(no_review_product.calculated_average_rating)
        self.assertIsNone(no_review_product.average_rating)