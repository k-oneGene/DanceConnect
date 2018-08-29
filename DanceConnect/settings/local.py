from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE', "pk_test_rfr8px0xKxm5HGvZ1dHxzvJv")
STRIPE_SECRET = os.environ.get('STRIPE_SECRET', "sk_test_nWwphAFJYtQ9iBle59hhKwOC")

INSTALLED_APPS += [
    'django_extensions',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
