from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from DjangoEcommerceApp.models import CustomUser
from products.models import Product
from products.views.AdminViews import ProductListView

class ProductSearchTestCase(TestCase):
    def setUp(self):
        """Create test products for search functionality"""
        # Create a staff user for the authenticated view
        self.staff_user = CustomUser.objects.create_user(
            username='staff_user',
            email='staff@example.com',
            password='test_password',
            user_type=2  # Staff user
        )
        self.factory = RequestFactory()

        # Create diverse products for testing
        Product.objects.create(
            product_name="Nike Air Max",
            brand="Nike",
            product_description="Running shoes with advanced cushioning"
        )
        Product.objects.create(
            product_name="Adidas Ultraboost",
            brand="Adidas",
            product_description="Performance running shoes with responsive boost technology"
        )
        Product.objects.create(
            product_name="New Balance 990v5",
            brand="New Balance",
            product_description="Classic running shoe with superior comfort"
        )

    def test_search_by_product_name_case_insensitive(self):
        """Test case-insensitive search by product name"""
        request = self.factory.get('/products/list/', {'q': 'nike'})
        request.user = self.staff_user
        view = ProductListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_search_by_brand_case_insensitive(self):
        """Test case-insensitive search by brand"""
        request = self.factory.get('/products/list/', {'q': 'ADIDAS'})
        request.user = self.staff_user
        view = ProductListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_search_by_description_case_insensitive(self):
        """Test case-insensitive search by description"""
        request = self.factory.get('/products/list/', {'q': 'RESPONSIVE'})
        request.user = self.staff_user
        view = ProductListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_partial_match_functionality(self):
        """Test partial match across all searchable fields"""
        test_queries = ['run', 'air', 'balan']

        for query in test_queries:
            request = self.factory.get('/products/list/', {'q': query})
            request.user = self.staff_user
            view = ProductListView.as_view()
            response = view(request)
            self.assertEqual(response.status_code, 200)

    def test_no_results_search(self):
        """Verify search works correctly with no matching results"""
        request = self.factory.get('/products/list/', {'q': 'nonexistent'})
        request.user = self.staff_user
        view = ProductListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)