from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from cdt.factories import UserFactory, PreferenciasFactory


class UserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse('tenants:user-list')

    def test_list_users(self):
        """Test that users can be listed"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)

    def test_create_user(self):
        """Test that a user can be created"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(User.objects.count(), 2)


class UserDetailAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('tenants:user-detail', args=[self.user.id])

    def test_get_user_detail(self):
        """Test that user details can be retrieved"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        """Test that user can be updated"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')


class PreferenciasAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.preferencias = PreferenciasFactory(user=self.user)
        self.url = reverse('tenants:preferencias-list')

    def test_get_preferencias(self):
        """Test that user preferences can be retrieved"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['tema_oscuro'], 
            self.preferencias.tema_oscuro
        )

    def test_create_preferencias(self):
        """Test that preferences can be created"""
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        data = {
            'tema_oscuro': True,
            'notificaciones_email': False,
            'notificaciones_push': True,
            'idioma': 'en'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['tema_oscuro'], 
            str(True)
        )
        self.assertEqual(response.data['idioma'], 'en')


class PreferenciasDetailAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.preferencias = PreferenciasFactory(user=self.user)
        self.url = reverse('tenants:preferencias-detail', args=[self.user.id])

    def test_get_preferencias_detail(self):
        """Test that specific user preferences can be retrieved"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['tema_oscuro'], 
            self.preferencias.tema_oscuro
        )

    def test_update_preferencias(self):
        """Test that preferences can be updated"""
        data = {
            'tema_oscuro': True,
            'notificaciones_email': False,
            'notificaciones_push': True,
            'idioma': 'en'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['tema_oscuro'], 
            str(True)
        )
        self.assertEqual(response.data['idioma'], 'en') 