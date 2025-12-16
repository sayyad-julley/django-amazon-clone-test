import pytest
from django.test import TestCase
from django.urls import reverse
from product.models import Product
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestProductListView(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        # Create a diverse set of test products
        self.products = [
            Product.objects.create(
                name='Laptop Pro',
                description='High-performance laptop for professionals',
                brand='TechBrand',
                price=1500.00
            ),
            Product.objects.create(
                name='Smartphone Elite',
                description='Advanced smartphone with cutting-edge features',
                brand='MobileTech',
                price=1200.00
            ),
            Product.objects.create(
                name='Wireless Headphones',
                description='Noise-cancelling headphones by TechBrand',
                brand='AudioGear',
                price=250.00
            ),
            Product.objects.create(
                name='budget laptop',
                description='Affordable laptop for everyday use',
                brand='EconomyTech',
                price=600.00
            )
        ]

        # Authenticate the test client
        self.client.login(username='testuser', password='12345')

    def test_search_exact_match(self):
        """Test searching with exact product name"""
        response = self.client.get(reverse('product_list'), {'search': 'Laptop Pro'})
        assert response.status_code == 200
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['product_list'][0].name, 'Laptop Pro')

    def test_search_case_insensitive(self):
        """Test case-insensitive search across multiple fields"""
        test_cases = [
            'laptop pro',
            'LAPTOP PRO',
            'LaPtOp PrO'
        ]

        for query in test_cases:
            response = self.client.get(reverse('product_list'), {'search': query})
            assert response.status_code == 200
            self.assertEqual(len(response.context['product_list']), 1)
            self.assertEqual(response.context['product_list'][0].name, 'Laptop Pro')

    def test_search_partial_match(self):
        """Test partial matching in different fields"""
        test_cases = [
            # Name partial match
            {'query': 'lap', 'expected_count': 2},
            {'query': 'phone', 'expected_count': 2},

            # Description partial match
            {'query': 'professional', 'expected_count': 1},
            {'query': 'affordable', 'expected_count': 1},

            # Brand partial match
            {'query': 'tech', 'expected_count': 3}
        ]

        for case in test_cases:
            response = self.client.get(reverse('product_list'), {'search': case['query']})
            assert response.status_code == 200
            self.assertEqual(
                len(response.context['product_list']),
                case['expected_count'],
                f"Failed for query: {case['query']}"
            )

    def test_search_multiple_fields(self):
        """Test searching across multiple product fields"""
        test_cases = [
            # Search across name and brand
            {'query': 'TechBrand', 'expected_names': ['Laptop Pro', 'Wireless Headphones']},

            # Search across description
            {'query': 'cutting-edge', 'expected_names': ['Smartphone Elite']},

            # Mixed field search
            {'query': 'professional', 'expected_names': ['Laptop Pro']}
        ]

        for case in test_cases:
            response = self.client.get(reverse('product_list'), {'search': case['query']})
            assert response.status_code == 200

            result_names = [product.name for product in response.context['product_list']]
            self.assertCountEqual(
                result_names,
                case['expected_names'],
                f"Failed for query: {case['query']}"
            )

    def test_pagination(self):
        """Test pagination functionality with search results"""
        # Create more products to test pagination
        for i in range(10):
            Product.objects.create(
                name=f'Test Product {i}',
                description=f'Test Description {i}',
                brand='PaginationBrand',
                price=100.00 + i
            )

        # Test default pagination (assuming 10 items per page)
        response = self.client.get(reverse('product_list'), {'page': 1})
        assert response.status_code == 200
        self.assertEqual(len(response.context['product_list']), 10)

        # Test pagination with search
        response = self.client.get(
            reverse('product_list'),
            {'search': 'PaginationBrand', 'page': 2}
        )
        assert response.status_code == 200
        self.assertTrue(len(response.context['product_list']) > 0)

    def test_no_results(self):
        """Test search with no matching results"""
        response = self.client.get(reverse('product_list'), {'search': 'NonexistentProduct'})
        assert response.status_code == 200
        self.assertEqual(len(response.context['product_list']), 0)

    def test_empty_search_query(self):
        """Test behavior with empty search query"""
        response = self.client.get(reverse('product_list'), {'search': ''})
        assert response.status_code == 200
        self.assertEqual(len(response.context['product_list']), 4)  # All products should be returned

    def tearDown(self):
        # Clean up created objects
        Product.objects.all().delete()
        User.objects.all().delete()