import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from backend.core.models import ConnectionRequest

User = get_user_model()

print("--- Users ---")
for u in User.objects.all():
    print(f"User: {u.username}, ID: {u.unique_id}, PK: {u.pk}")

print("\n--- Connection Requests ---")
for cr in ConnectionRequest.objects.all():
    print(f"Sender: {cr.sender.username} -> Receiver: {cr.receiver.username}, Status: {cr.status}")
