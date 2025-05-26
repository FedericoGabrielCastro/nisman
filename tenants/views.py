from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Tenant
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
        return Response([{
            'id': tenant.id,
            'name': tenant.name,
            'schema_name': tenant.schema_name,
            'domain': tenant.domain,
            'is_active': tenant.is_active,
            'created_at': tenant.created_at,
            'updated_at': tenant.updated_at
        } for tenant in tenants])

    def post(self, request):
        """
        POST /api/tenants/
        Create a new tenant
        """
        tenant = Tenant.objects.create(
            name=request.data.get('name'),
            schema_name=request.data.get('schema_name'),
            domain=request.data.get('domain'),
            is_active=request.data.get('is_active', True)
        )
        return Response({
            'id': tenant.id,
            'name': tenant.name,
            'schema_name': tenant.schema_name,
            'domain': tenant.domain,
            'is_active': tenant.is_active,
            'created_at': tenant.created_at,
            'updated_at': tenant.updated_at
        }, status=status.HTTP_201_CREATED)


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
        return Response({
            'id': tenant.id,
            'name': tenant.name,
            'schema_name': tenant.schema_name,
            'domain': tenant.domain,
            'is_active': tenant.is_active,
            'created_at': tenant.created_at,
            'updated_at': tenant.updated_at
        })

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

        tenant.name = request.data.get('name', tenant.name)
        tenant.schema_name = request.data.get('schema_name', tenant.schema_name)
        tenant.domain = request.data.get('domain', tenant.domain)
        tenant.is_active = request.data.get('is_active', tenant.is_active)
        tenant.save()
        
        return Response({
            'id': tenant.id,
            'name': tenant.name,
            'schema_name': tenant.schema_name,
            'domain': tenant.domain,
            'is_active': tenant.is_active,
            'created_at': tenant.created_at,
            'updated_at': tenant.updated_at
        })


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
        Tenant.objects.create(
            name=username,
            schema_name=username,
            domain=f'{username}.example.com',
            is_active=True
        )
        return Response(
            {'message': f'Tenant "{username}" created successfully'}, 
            status=status.HTTP_201_CREATED
        )
