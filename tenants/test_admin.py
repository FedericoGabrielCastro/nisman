from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from .models import Tenant
from .admin import TenantAdmin
from .factories import TenantFactory
from cdt.factories import UserFactory


class TenantAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.client.force_login(self.user)
        self.tenant = TenantFactory()

    def test_tenant_admin_listed(self):
        url = reverse('admin:tenants_tenant_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tenant.name)

    def test_tenant_admin_change(self):
        url = reverse('admin:tenants_tenant_change', args=[self.tenant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tenant.name)

    def test_tenant_admin_add(self):
        url = reverse('admin:tenants_tenant_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tenant') 