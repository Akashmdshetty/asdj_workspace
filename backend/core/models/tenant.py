from django.db import models
from django.conf import settings
from .user import User

class Tenant(models.Model):
    """
    Represents a workspace or organization.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,
        related_name='owned_tenants'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
