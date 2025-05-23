from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Preferencias
from .factories import UserFactory, PreferenciasFactory
from .exceptions import InvalidUsernameException, UserAlreadyExistsException

# Create your views here.

class UserAPIView(APIView):
    """
    API endpoint for user operations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        GET /api/users/
        List all users
        """
        users = User.objects.all()
        return Response([{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        } for user in users])

    def post(self, request):
        """
        POST /api/users/
        Create a new user
        """
        try:
            user = User.objects.create_user(
                username=request.data.get('username'),
                email=request.data.get('email'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name', ''),
                last_name=request.data.get('last_name', '')
            )
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """
    API endpoint for specific user operations
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        GET /api/users/{user_id}/
        Get specific user details
        """
        user = get_object_or_404(User, id=user_id)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    def put(self, request, user_id):
        """
        PUT /api/users/{user_id}/
        Update specific user
        """
        user = get_object_or_404(User, id=user_id)
        if request.user != user and not request.user.is_staff:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.email = request.data.get('email', user.email)
            if 'password' in request.data:
                user.set_password(request.data['password'])
            user.save()
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PreferenciasAPIView(APIView):
    """
    API endpoint for user preferences
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        GET /api/preferencias/
        Get current user's preferences
        """
        try:
            preferencias = Preferencias.objects.get(user=request.user)
            return Response({
                'tema_oscuro': preferencias.tema_oscuro,
                'notificaciones_email': preferencias.notificaciones_email,
                'notificaciones_push': preferencias.notificaciones_push,
                'idioma': preferencias.idioma
            })
        except Preferencias.DoesNotExist:
            return Response({'error': 'No preferences found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        POST /api/preferencias/
        Create preferences for current user
        """
        try:
            preferencias = Preferencias.objects.create(
                user=request.user,
                tema_oscuro=request.data.get('tema_oscuro', False),
                notificaciones_email=request.data.get('notificaciones_email', True),
                notificaciones_push=request.data.get('notificaciones_push', True),
                idioma=request.data.get('idioma', 'es')
            )
            return Response({
                'tema_oscuro': preferencias.tema_oscuro,
                'notificaciones_email': preferencias.notificaciones_email,
                'notificaciones_push': preferencias.notificaciones_push,
                'idioma': preferencias.idioma
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PreferenciasDetailAPIView(APIView):
    """
    API endpoint for specific user preferences
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        GET /api/preferencias/{user_id}/
        Get specific user's preferences
        """
        if request.user.id != user_id and not request.user.is_staff:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            preferencias = Preferencias.objects.get(user_id=user_id)
            return Response({
                'tema_oscuro': preferencias.tema_oscuro,
                'notificaciones_email': preferencias.notificaciones_email,
                'notificaciones_push': preferencias.notificaciones_push,
                'idioma': preferencias.idioma
            })
        except Preferencias.DoesNotExist:
            return Response({'error': 'No preferences found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        """
        PUT /api/preferencias/{user_id}/
        Update specific user's preferences
        """
        if request.user.id != user_id and not request.user.is_staff:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        try:
            preferencias = Preferencias.objects.get(user_id=user_id)
            preferencias.tema_oscuro = request.data.get('tema_oscuro', preferencias.tema_oscuro)
            preferencias.notificaciones_email = request.data.get('notificaciones_email', preferencias.notificaciones_email)
            preferencias.notificaciones_push = request.data.get('notificaciones_push', preferencias.notificaciones_push)
            preferencias.idioma = request.data.get('idioma', preferencias.idioma)
            preferencias.save()
            return Response({
                'tema_oscuro': preferencias.tema_oscuro,
                'notificaciones_email': preferencias.notificaciones_email,
                'notificaciones_push': preferencias.notificaciones_push,
                'idioma': preferencias.idioma
            })
        except Preferencias.DoesNotExist:
            return Response({'error': 'No preferences found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NismanAPIView(APIView):
    """
    API endpoint for /nisman POST
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Get the username from the request data
        username = request.data.get('username', '')

        # Validate that the username is not empty
        if not username.strip():
            raise InvalidUsernameException()

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            raise UserAlreadyExistsException()

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='securepassword'
        )
        return Response({'message': f'User "{username}" created successfully'}, status=status.HTTP_201_CREATED)
