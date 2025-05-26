from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Tenant
from .serializers import TenantSerializer
from .exceptions import InvalidUsernameException, UserAlreadyExistsException


class TenantsAPIView(APIView):
    """
    API endpoint for tenants operations
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        GET /api/tenants/
        List all tenants
        """
        tenants = Tenant.objects.all()
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /api/tenants/
        Create a new tenant
        """
        serializer = TenantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save()
        return Response(
            TenantSerializer(tenant).data,
            status=status.HTTP_201_CREATED
        )


class TenantDetailAPIView(APIView):
    """
    API endpoint for specific tenant operations
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, tenant_id):
        """
        GET /api/tenants/{tenant_id}/
        Get specific tenant details
        """
        tenant = get_object_or_404(Tenant, id=tenant_id)
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    def put(self, request, tenant_id):
        """
        PUT /api/tenants/{tenant_id}/
        Update specific tenant
        """
        tenant = get_object_or_404(Tenant, id=tenant_id)
        if not request.user.is_staff:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TenantSerializer(tenant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save()
        return Response(TenantSerializer(tenant).data)


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
        if Tenant.objects.filter(name=username).exists():
            raise UserAlreadyExistsException()

        # Create the tenant
        data = {
            'name': username,
            'schema_name': username,
            'domain': f'{username}.example.com',
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {'message': f'Tenant "{username}" created successfully'}, 
            status=status.HTTP_201_CREATED
        )
