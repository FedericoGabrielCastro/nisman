from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .exceptions import InvalidUsernameException, UserAlreadyExistsException


class TenantsAPIView(APIView):
    """
    API endpoint for tenants operations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        GET /api/tenants/
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
        POST /api/tenants/
        Create a new user
        """
        
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


class NismanAPIView(APIView):
    """
    API endpoint for /tenants/nisman POST
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
        User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='securepassword'
        )
        return Response(
            {'message': f'User "{username}" created successfully'}, 
            status=status.HTTP_201_CREATED
        )
