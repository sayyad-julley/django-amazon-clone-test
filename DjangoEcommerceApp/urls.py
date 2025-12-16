from django.urls import path
from DjangoEcommerceApp import views

urlpatterns = [
    path('', views.demoPage, name="home"),
    path('auth/login/', views.login_user_view, name="login"),
    path('auth/register/', views.register_user_view, name="register"),
    path('auth/logout/', views.logout_user_view, name="logout"),
    path('auth/password-reset/', views.password_reset_request, name="password_reset_request"),
    path('api/auth/login/', views.api_login_view, name="api_login"),
    path('admin_login_process', views.adminLoginProcess, name="admin_login_process"),
    path('admin_logout_process', views.adminLogoutProcess, name="admin_logout_process"),
]
