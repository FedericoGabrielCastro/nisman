from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Preferencias

class UserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-list')

    def test_get_users(self):
        # Create a test user
        User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())


class PreferenciasAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('preferencias')
        # Create a test user and preferences
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.preferencias = Preferencias.objects.create(
            user=self.user,
            tema_oscuro=True,
            notificaciones_email=False,
            notificaciones_push=True,
            idioma='es'
        )
        # Authenticate the client
        self.client.force_authenticate(user=self.user)

    def test_get_preferencias(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tema_oscuro'], True)
        self.assertEqual(response.data['notificaciones_email'], False)
        self.assertEqual(response.data['notificaciones_push'], True)
        self.assertEqual(response.data['idioma'], 'es')

    def test_create_preferencias(self):
        # Create a new user for this test
        new_user = User.objects.create_user(username='newuser', email='new@example.com', password='newpass')
        # Authenticate as the new user
        self.client.force_authenticate(user=new_user)
        
        data = {
            'tema_oscuro': False,
            'notificaciones_email': True,
            'notificaciones_push': False,
            'idioma': 'en'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['tema_oscuro'], False)
        self.assertEqual(response.data['notificaciones_email'], True)
        self.assertEqual(response.data['notificaciones_push'], False)
        self.assertEqual(response.data['idioma'], 'en')
        self.assertTrue(Preferencias.objects.filter(user=new_user).exists()) 