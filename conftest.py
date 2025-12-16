import os
import django
from django.conf import settings

# Configure Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'DjangoEcommerceApp',
    'products',
    'accounts',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Configure Django settings
settings.configure(
    DEBUG=True,
    INSTALLED_APPS=INSTALLED_APPS,
    DATABASES=DATABASES,
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    SECRET_KEY='test_secret_key',
    AUTH_USER_MODEL='DjangoEcommerceApp.CustomUser',
)

# Setup Django
django.setup()

def pytest_configure(config):
    """
    Allows plugins and fixtures to be used before making any imports
    """
    config.addinivalue_line(
        "markers",
        "django_db: mark test to require django database setup",
    )