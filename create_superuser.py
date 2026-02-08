import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'aakashdshetty'
email = 'aakashdshetty@example.com'
password = 'asda3539'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
