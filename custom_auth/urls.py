from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),

    # Web interface routes
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # API routes
    path('api/login/', views.api_login_view, name='api_login'),
]