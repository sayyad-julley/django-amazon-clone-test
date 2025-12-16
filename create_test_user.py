import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoEcommerce.settings')
django.setup()

from DjangoEcommerceApp.models import CustomUser

username = "testuser"
password = "testpass123"
email = "testuser@example.com"

if not CustomUser.objects.filter(username=username).exists():
    print(f"Creating user {username}...")
    user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=4)
    user.save()
    print("User created.")
else:
    print(f"User {username} already exists.")
