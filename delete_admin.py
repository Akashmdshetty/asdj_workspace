import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    user = User.objects.get(username='admin')
    user.delete()
    print("User 'admin' deleted successfully.")
except User.DoesNotExist:
    print("User 'admin' does not exist.")
