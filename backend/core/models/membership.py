from django.db import models
from django.conf import settings
from .tenant import Tenant

class Membership(models.Model):
    """
    Linking table between User and Tenant with roles.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tenant')

    def __str__(self):
        return f"{self.user} in {self.tenant} as {self.role}"
