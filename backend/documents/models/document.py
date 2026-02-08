from django.db import models
from django.conf import settings
from backend.core.models import Tenant
from .folder import Folder

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default='')
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_documents'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.tenant})"
