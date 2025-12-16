from django.test import TestCase, override_settings
from DjangoEcommerceApp.models import CustomUser
from DjangoEcommerceApp.models import Products, MerchantUser, SubCategories, Categories
from django.urls import reverse
from django.urls import path
from DjangoEcommerceApp.AdminViews import ProductListView

urlpatterns = [
    path('admin/product-list/', ProductListView.as_view(), name='product_list'),
]

@override_settings(ROOT_URLCONF=__name__)
class ProductSearchTestCase(TestCase):
    def setUp(self):
        # Create a merchant user
        self.merchant_user = CustomUser.objects.create_user(
            username='testmerchant',
            password='testpass',
            email='testmerchant@example.com',
            user_type=3,  # Assuming 3 is for merchant users
            is_active=True
        )
        merchant_profile, _ = MerchantUser.objects.get_or_create(auth_user_id=self.merchant_user)

        # Log in the user for the tests
        self.client.login(username='testmerchant', password='testpass')

        # Create a category
        self.category = Categories.objects.create(
            title='Test Category',
            description='Test Category Description',
            is_active=True
        )

        # Create a subcategory
        self.subcategory = SubCategories.objects.create(
            title='Test Subcategory',
            is_active=True,
            category_id=self.category
        )

        # Create test products with varied names, descriptions, and brands
        self.product1 = Products.objects.create(
            product_name='Nike Running Shoes First Model',
            product_description='High-performance running shoes made by Nike',
            brand='Nike Classic',
            added_by_merchant=merchant_profile,
            subcategories_id=self.subcategory
        )
        self.product2 = Products.objects.create(
            product_name='Adidas Football Cleats Pro Edition',
            product_description='Professional football cleats with excellent grip from Adidas',
            brand='Adidas Pro',
            added_by_merchant=merchant_profile,
            subcategories_id=self.subcategory
        )
        self.product3 = Products.objects.create(
            product_name='Casual Sneakers Urban Style',
            product_description='Comfortable everyday sneakers with urban design',
            brand='Puma Urban',
            added_by_merchant=merchant_profile,
            subcategories_id=self.subcategory
        )

    def test_case_insensitive_product_name_search(self):
        """Test case-insensitive search by product name"""
        search_queries = ['nike', 'NIKE', 'NiKe']
        for query in search_queries:
            response = self.client.get(reverse('product_list'), {'filter': query})
            self.assertEqual(response.status_code, 200)
            products_list = response.context['object_list']
            # Expect 1 product with Nike in the name
            self.assertEqual(len(products_list), 1, f"Failed for query: {query}")
            self.assertEqual(products_list[0]['product'].product_name, 'Nike Running Shoes First Model')

    def test_case_insensitive_brand_search(self):
        """Test case-insensitive search by brand"""
        search_queries = ['nike classic', 'NIKE CLASSIC', 'NiKe ClAsSiC']
        for query in search_queries:
            response = self.client.get(reverse('product_list'), {'filter': query})
            self.assertEqual(response.status_code, 200)
            products_list = response.context['object_list']
            # Expect 1 product with Nike Classic as the brand
            self.assertEqual(len(products_list), 1, f"Failed for query: {query}")
            self.assertEqual(products_list[0]['product'].brand, 'Nike Classic')

    def test_case_insensitive_description_search(self):
        """Test case-insensitive search by description"""
        search_queries = ['running', 'RUNNING', 'RuNnInG']
        for query in search_queries:
            response = self.client.get(reverse('product_list'), {'filter': query})
            self.assertEqual(response.status_code, 200)
            products_list = response.context['object_list']
            # Expect 1 product with 'running' in the description
            self.assertEqual(len(products_list), 1, f"Failed for query: {query}")
            self.assertEqual(
                products_list[0]['product'].product_description,
                'High-performance running shoes made by Nike'
            )

    def test_partial_match_search(self):
        """Test partial match search across name, brand, and description"""
        search_queries = [
            'run',     # Partial match in description
            'nik',     # Partial match in name and description
            'foot'     # Partial match in description
        ]
        expected_results = {
            'run': ['Nike Running Shoes First Model'],
            'nik': ['Nike Running Shoes First Model'],
            'foot': ['Adidas Football Cleats Pro Edition']
        }
        for query in search_queries:
            response = self.client.get(reverse('product_list'), {'filter': query})
            self.assertEqual(response.status_code, 200)
            products_list = response.context['object_list']

            # Check that the correct product is returned
            self.assertEqual(len(products_list), 1, f"Failed for query: {query}")
            self.assertEqual(products_list[0]['product'].product_name, expected_results[query][0])

    def test_multi_result_search(self):
        """Test search query that returns multiple results"""
        response = self.client.get(reverse('product_list'), {'filter': 'sneakers'})
        self.assertEqual(response.status_code, 200)
        products_list = response.context['object_list']
        # Expect 1 product with 'sneakers' in the description
        self.assertEqual(len(products_list), 1)
        self.assertEqual(products_list[0]['product'].product_name, 'Casual Sneakers Urban Style')