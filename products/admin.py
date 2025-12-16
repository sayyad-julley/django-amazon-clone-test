from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'display_average_rating', 'created_at']
    list_filter = ['brand']
    search_fields = ['product_name', 'brand']

    def display_average_rating(self, obj):
        """
        Display average rating in admin with a nice format
        """
        return obj.average_rating or 'No Ratings'
    display_average_rating.short_description = 'Average Rating'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['product__product_name', 'user__username']