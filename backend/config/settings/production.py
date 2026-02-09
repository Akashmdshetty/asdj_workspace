
from .base import *
import os
import dj_database_url
import sys
from pathlib import Path

# DEBUGGING PATHS REVISED
print(f"DEBUG: BASE_DIR = {BASE_DIR}")
print(f"DEBUG: BASE_DIR.parent = {BASE_DIR.parent}")

print("DEBUG: Listing BASE_DIR.parent (SRC root):")
try:
    print(os.listdir(BASE_DIR.parent))
except Exception as e:
    print(f"Error listing parent: {e}")

print("DEBUG: Checking for frontend/dist in BASE_DIR.parent:")
frontend_dist = BASE_DIR.parent / "frontend" / "dist"
print(f"DEBUG: Looking for {frontend_dist}")
if frontend_dist.exists():
    print(f"DEBUG: FOUND! Contents: {os.listdir(frontend_dist)}")
    # FIXING THE PATHS DYNAMICALLY
    TEMPLATE_DIR = frontend_dist
    STATIC_DIR = frontend_dist
else:
    print("DEBUG: NOT FOUND.")
    TEMPLATE_DIR = BASE_DIR / "frontend/dist" # Fallback (broken)
    STATIC_DIR = BASE_DIR / "frontend/dist"

DEBUG = os.environ.get("DEBUG", "False") == "True"

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-in-production")

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.fly.dev",
]


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
    # BASE_DIR / "frontend/dist", # Original broken
    BASE_DIR.parent / "frontend" / "dist", # Try this explicitly
]

# Configure Templates to look in frontend/dist
# Remove the old incorrect append and use the resolved path
for template in TEMPLATES:
    # template['DIRS'].append(BASE_DIR / "frontend/dist") # Incorrect based on logs
    template['DIRS'].append(BASE_DIR.parent / "frontend" / "dist")

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
