from django.test import TestCase
from django.contrib.auth.models import User
from .models import Preferencias
from .serializers import UserSerializer, PreferenciasSerializer, UserWithPreferenciasSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='testpass123',
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {'id', 'username', 'email', 'first_name', 'last_name'}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_read_only_fields(self):
        """Test that read-only fields cannot be modified"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'id': 999
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotEqual(user.id, 999)

    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_update_user(self):
        """Test updating an existing user"""
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        serializer = UserSerializer(
            instance=self.user,
            data=data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(user.first_name, 'Test')  # Unchanged
        self.assertEqual(user.last_name, 'User')   # Unchanged

    def test_validation_username(self):
        """Test username validation"""
        # Create a user with the username we want to test
        User.objects.create_user(
            username='test_username',
            email='first@example.com'
        )
        # Try to create another user with the same username
        data = {
            'username': 'test_username',
            'email': 'second@example.com',
            'first_name': 'Second',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_validation_email(self):
        """Test email validation"""
        # Create a user with the email we want to test
        User.objects.create_user(
            username='first_user',
            email='test@example.com'
        )
        # Try to create another user with the same email
        data = {
            'username': 'second_user',
            'email': 'test@example.com',  # Same email as first user
            'first_name': 'Second',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class PreferenciasSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.preferencias_data = {
            'tema_oscuro': True,
            'notificaciones_email': True,
            'notificaciones_push': False,
            'idioma': 'es'
        }
        self.preferencias = Preferencias.objects.create(
            user=self.user,
            **self.preferencias_data
        )
        self.serializer = PreferenciasSerializer(instance=self.preferencias)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {
            'tema_oscuro',
            'notificaciones_email',
            'notificaciones_push',
            'idioma'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_create_preferencias(self):
        """Test creating new preferences"""
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com'
        )
        data = {
            'tema_oscuro': False,
            'notificaciones_email': True,
            'notificaciones_push': True,
            'idioma': 'en'
        }
        serializer = PreferenciasSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        preferencias = serializer.save(user=user)
        self.assertEqual(preferencias.tema_oscuro, False)
        self.assertEqual(preferencias.notificaciones_email, True)
        self.assertEqual(preferencias.notificaciones_push, True)
        self.assertEqual(preferencias.idioma, 'en')

    def test_update_preferencias(self):
        """Test updating existing preferences"""
        data = {
            'tema_oscuro': False,
            'idioma': 'en'
        }
        serializer = PreferenciasSerializer(
            instance=self.preferencias,
            data=data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        preferencias = serializer.save()
        self.assertEqual(preferencias.tema_oscuro, False)
        self.assertEqual(preferencias.idioma, 'en')
        self.assertEqual(preferencias.notificaciones_email, True)  # Unchanged
        self.assertEqual(preferencias.notificaciones_push, False)  # Unchanged


class UserWithPreferenciasSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.preferencias = Preferencias.objects.create(
            user=self.user,
            tema_oscuro=True,
            notificaciones_email=True,
            notificaciones_push=False,
            idioma='es'
        )
        self.serializer = UserWithPreferenciasSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'preferencias'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_preferencias_data(self):
        """Test that preferences data is correctly included"""
        data = self.serializer.data
        self.assertIn('preferencias', data)
        preferencias_data = data['preferencias']
        self.assertEqual(preferencias_data['tema_oscuro'], True)
        self.assertEqual(preferencias_data['notificaciones_email'], True)
        self.assertEqual(preferencias_data['notificaciones_push'], False)
        self.assertEqual(preferencias_data['idioma'], 'es')

    def test_read_only_preferencias(self):
        """Test that preferences cannot be modified through this serializer"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'preferencias': {
                'tema_oscuro': False,
                'idioma': 'en'
            }
        }
        serializer = UserWithPreferenciasSerializer(
            instance=self.user,
            data=data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        # Preferences should remain unchanged
        self.assertEqual(user.preferencias.tema_oscuro, True)
        self.assertEqual(user.preferencias.idioma, 'es') 