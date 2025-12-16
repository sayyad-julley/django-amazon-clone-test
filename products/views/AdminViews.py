from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'admin/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Number of products per page

    def get_queryset(self):
        """
        Enhanced queryset with case-insensitive, partial match search
        across multiple product fields
        """
        # Check if the user is staff or superuser
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            return Product.objects.none()

        queryset = super().get_queryset()

        # Get search query from GET parameters
        search_query = self.request.GET.get('q', '').strip()

        if search_query:
            # Use Q objects for complex OR filtering
            search_filter = (
                Q(product_name__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(product_description__icontains=search_query)
            )
            queryset = queryset.filter(search_filter)

        # Order by most recently added products first
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Add additional context for search and pagination
        """
        context = super().get_context_data(**kwargs)

        # Add search query to context for preserving in template
        context['search_query'] = self.request.GET.get('q', '')

        # Optional: Add more context if needed for admin dashboard
        context['total_products'] = self.get_queryset().count()

        return context