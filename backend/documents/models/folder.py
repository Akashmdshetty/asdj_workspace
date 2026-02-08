from django.db import models
from django.conf import settings
from backend.core.models import Tenant

class Folder(models.Model):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='folders'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfolders'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_folders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'parent', 'name')

    def __str__(self):
        return f"{self.name} ({self.tenant})"
