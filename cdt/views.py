from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Preferencias

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

class PreferenciasAPIView(APIView):
    """
    API endpoint for user preferences
    """
    permission_classes = [permissions.AllowAny]

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
