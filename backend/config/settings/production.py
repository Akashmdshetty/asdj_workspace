
from .base import *
import os
import dj_database_url
import sys

# DEBUGGING PATHS
print(f"DEBUG: BASE_DIR = {BASE_DIR}")
print(f"DEBUG: BASE_DIR parent = {BASE_DIR.parent}")
print(f"DEBUG: frontend/dist exists? = {(BASE_DIR / 'frontend/dist').exists()}")
if (BASE_DIR / 'frontend/dist').exists():
    print(f"DEBUG: frontend/dist listing: {os.listdir(BASE_DIR / 'frontend/dist')}")
else:
    print(f"DEBUG: frontend/dist does NOT exist at {BASE_DIR / 'frontend/dist'}")
    # Try looking one level up just in case
    print(f"DEBUG: ../frontend/dist exists? = {(BASE_DIR / '../frontend/dist').resolve().exists()}")


DEBUG = os.environ.get("DEBUG", "False") == "True"

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-in-production")

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Middleware: Add WhiteNoise for static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Add frontend build to static files
STATICFILES_DIRS = [
    BASE_DIR / "frontend/dist",
]

# Configure Templates to look in frontend/dist
# Ensure we update the settings imported from base
for template in TEMPLATES:
    template['DIRS'].append(BASE_DIR / "frontend/dist")

# Channel Layer for Production (Redis)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# Celery
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')
