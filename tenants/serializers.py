from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tenant model
    """
    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'schema_name',
            'domain',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 