from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from .models import Preferencias
from .admin import PreferenciasAdmin
from .factories import PreferenciasFactory, UserFactory


class PreferenciasAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.client.force_login(self.user)
        self.preferencias = PreferenciasFactory()

    def test_preferencias_admin_listed(self):
        url = reverse('admin:cdt_preferencias_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.preferencias.user.username)

    def test_preferencias_admin_change(self):
        url = reverse('admin:cdt_preferencias_change', args=[self.preferencias.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.preferencias.user.username)

    def test_preferencias_admin_add(self):
        url = reverse('admin:cdt_preferencias_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Preferencias') 