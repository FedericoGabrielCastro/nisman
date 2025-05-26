from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Preferencias
from .factories import UserFactory, PreferenciasFactory
from .exceptions import (
    InvalidUsernameException, UserAlreadyExistsException,
    UserIdRequiredException, UserNotFoundException,
    PreferenciasNotFoundException, ValidationException
)
from .serializers import UserSerializer, PreferenciasSerializer, UserWithPreferenciasSerializer

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
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /api/users/
        Create a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                password=request.data.get('password'),
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', '')
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        raise ValidationException(serializer.errors)


class UserDetailAPIView(APIView):
    """
    API endpoint for specific user operations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        """
        GET /api/users/{user_id}/
        Get specific user details
        """
        user = User.objects.get(id=user_id)
        serializer = UserWithPreferenciasSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        """
        PUT /api/users/{user_id}/
        Update specific user
        """
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                user.set_password(request.data['password'])
            serializer.save()
            return Response(UserSerializer(user).data)
        raise ValidationException(serializer.errors)


class PreferenciasAPIView(APIView):
    """
    API endpoint for user preferences
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        GET /api/preferencias/
        Get preferences by user_id
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            raise UserIdRequiredException()
            
        user = User.objects.get(id=user_id)
        preferencias = Preferencias.objects.get(user=user)
        serializer = PreferenciasSerializer(preferencias)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /api/preferencias/
        Create preferences for a user
        """
        user_id = request.data.get('user_id')
        if not user_id:
            raise UserIdRequiredException()

        user = User.objects.get(id=user_id)
        serializer = PreferenciasSerializer(data=request.data)
        if serializer.is_valid():
            preferencias = serializer.save(user=user)
            return Response(PreferenciasSerializer(preferencias).data, status=status.HTTP_201_CREATED)
        raise ValidationException(serializer.errors)


class PreferenciasDetailAPIView(APIView):
    """
    API endpoint for specific user preferences
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        """
        GET /api/preferencias/{user_id}/
        Get specific user's preferences
        """
        preferencias = Preferencias.objects.get(user_id=user_id)
        serializer = PreferenciasSerializer(preferencias)
        return Response(serializer.data)

    def put(self, request, user_id):
        """
        PUT /api/preferencias/{user_id}/
        Update specific user's preferences
        """
        preferencias = Preferencias.objects.get(user_id=user_id)
        serializer = PreferenciasSerializer(preferencias, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ValidationException(serializer.errors)


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
