from django.contrib import admin
from DjangoEcommerceApp.models import Categories, SubCategories, Products

# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_slug')

@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_id', 'url_slug')

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand', 'average_rating')
    list_filter = ('brand',)
    search_fields = ('product_name', 'brand')
    readonly_fields = ('average_rating', 'dynamic_average_rating')

    def get_readonly_fields(self, request, obj=None):
        """
        Make average_rating read-only in the admin interface
        """
        return self.readonly_fields