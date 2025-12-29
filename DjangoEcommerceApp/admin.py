from django.contrib import admin
from DjangoEcommerceApp.models import Categories, SubCategories, Products

# Register your models here.
admin.site.register(Categories)
admin.site.register(SubCategories)

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'in_stock', 'in_stock_total')
    list_filter = ('in_stock',)
    list_editable = ('in_stock',)