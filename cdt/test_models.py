from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Preferencias
from .factories import PreferenciasFactory, UserFactory


class PreferenciasModelTest(TestCase):
    def setUp(self):
        self.preferencias = PreferenciasFactory()

    def test_preferencias_creation(self):
        """Test that preferencias can be created with valid data"""
        self.assertIsInstance(self.preferencias, Preferencias)
        self.assertIsInstance(self.preferencias.user, User)
        self.assertFalse(self.preferencias.tema_oscuro)
        self.assertTrue(self.preferencias.notificaciones_email)
        self.assertTrue(self.preferencias.notificaciones_push)
        self.assertEqual(self.preferencias.idioma, 'es')

    def test_preferencias_str_method(self):
        """Test the string representation of preferencias"""
        expected_str = f'Preferencias de {self.preferencias.user.username}'
        self.assertEqual(str(self.preferencias), expected_str)

    def test_one_to_one_relationship(self):
        """Test that a user can only have one preferencias instance"""
        with self.assertRaises(Exception):
            PreferenciasFactory(user=self.preferencias.user)

    def test_default_values(self):
        """Test that default values are set correctly"""
        new_preferencias = PreferenciasFactory()
        self.assertFalse(new_preferencias.tema_oscuro)
        self.assertTrue(new_preferencias.notificaciones_email)
        self.assertTrue(new_preferencias.notificaciones_push)
        self.assertEqual(new_preferencias.idioma, 'es')

    def test_custom_values(self):
        """Test that custom values can be set"""
        user = UserFactory()
        preferencias = PreferenciasFactory(
            user=user,
            tema_oscuro=True,
            notificaciones_email=False,
            notificaciones_push=False,
            idioma='en'
        )
        self.assertTrue(preferencias.tema_oscuro)
        self.assertFalse(preferencias.notificaciones_email)
        self.assertFalse(preferencias.notificaciones_push)
        self.assertEqual(preferencias.idioma, 'en') 