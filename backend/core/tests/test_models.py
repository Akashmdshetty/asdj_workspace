from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tenant, Membership

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))

class TenantModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', email='owner@test.com', password='password')

    def test_create_tenant(self):
        tenant = Tenant.objects.create(name="My Workspace", slug="my-workspace", owner=self.user)
        self.assertEqual(tenant.name, "My Workspace")
        self.assertEqual(tenant.owner, self.user)

    def test_membership_creation(self):
        tenant = Tenant.objects.create(name="Team", slug="team", owner=self.user)
        member = User.objects.create_user(username='member', email='member@test.com', password='password')
        
        membership = Membership.objects.create(user=member, tenant=tenant, role='member')
        self.assertEqual(membership.user, member)
        self.assertEqual(membership.tenant, tenant)
        self.assertEqual(membership.role, 'member')
