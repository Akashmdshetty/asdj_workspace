from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Use stdout for email in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS Settings for local development
CORS_ALLOW_ALL_ORIGINS = True
