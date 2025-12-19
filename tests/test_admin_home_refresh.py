from django.test import TestCase, Client
from django.urls import reverse
from DjangoEcommerceApp.models import CustomUser, Products, MerchantUser, SubCategories, Categories

class AdminHomeRefreshTestCase(TestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_user = CustomUser.objects.create_superuser(
            username='testadmin',
            email='admin@example.com',
            password='testpassword'
        )

        # Create a test merchant user
        merchant_auth_user = CustomUser.objects.create(
            username='testmerchant',
            email='merchant@example.com',
            password='testpassword'
        )
        merchant = MerchantUser.objects.create(
            auth_user_id=merchant_auth_user,
            company_name='Test Company',
            gst_details='GST123',
            address='Test Address'
        )

        # Create a test category and subcategory
        category = Categories.objects.create(
            title='Test Category',
            url_slug='test-category'
        )
        subcategory = SubCategories.objects.create(
            title='Test Subcategory',
            category_id=category,
            url_slug='test-subcategory',
            thumbnail=None,  # Use None as FileField might require upload
            description='Test Description'
        )

        # Create a test product with the merchant
        Products.objects.create(
            product_name='Test Product 1',
            added_by_merchant=merchant,
            subcategories_id=subcategory,
            url_slug='test-product-1',
            product_max_price='100',
            product_discount_price='90',
            brand='Test Brand',
            product_description='Test Description',
            product_long_description='Long Test Description'
        )

    def test_refresh_button_presence(self):
        # Log in the admin user
        self.client.login(username='testadmin', password='testpassword')

        # Get the admin home page
        response = self.client.get(reverse('admin_home'))

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Check for refresh button presence
        self.assertContains(response, 'btn btn-primary')
        self.assertContains(response, 'fa-sync-alt')
        self.assertContains(response, 'Refresh')

    def test_refresh_button_url(self):
        # Log in the admin user
        self.client.login(username='testadmin', password='testpassword')

        # Get the admin home page
        response = self.client.get(reverse('admin_home'))

        # Check refresh button URL
        self.assertContains(response, reverse('admin_home'))

    def test_unauthorized_access(self):
        # Try to access without login
        response = self.client.get(reverse('admin_home'))

        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        
        # Print out the actual redirect URL
        print(f"Redirect URL: {response.url}")
        
        # Test redirect logic 
        self.assertTrue(response.url.startswith('/'))

    def test_page_content(self):
        # Log in the admin user
        self.client.login(username='testadmin', password='testpassword')

        # Get the admin home page
        response = self.client.get(reverse('admin_home'))

        # Check total products count
        self.assertContains(response, 'Total Products: 1')

    def test_refresh_functionality(self):
        # Log in the admin user
        self.client.login(username='testadmin', password='testpassword')

        # Get the admin home page twice to ensure no side effects
        response1 = self.client.get(reverse('admin_home'))
        response2 = self.client.get(reverse('admin_home'))

        # Content should be consistent
        self.assertEqual(response1.content, response2.content)
