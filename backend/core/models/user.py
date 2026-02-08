from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for the SaaS application.
    """
    email = models.EmailField(unique=True)
    unique_id = models.CharField(max_length=6, unique=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            import random
            import string
            while True:
                uid = ''.join(random.choices(string.digits, k=6))
                if not User.objects.filter(unique_id=uid).exists():
                    self.unique_id = uid
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.unique_id})"
