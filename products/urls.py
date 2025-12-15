from django.urls import path
from products.views.AdminViews import ProductListView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
]