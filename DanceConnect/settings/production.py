from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE', "pk_test_rfr8px0xKxm5HGvZ1dHxzvJv")
STRIPE_SECRET = os.environ.get('STRIPE_SECRET', "sk_test_nWwphAFJYtQ9iBle59hhKwOC")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


#TODO: TEMP UNTIL SSL IS ADDED
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'http')
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = False
