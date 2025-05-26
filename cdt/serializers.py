from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Preferencias


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate_email(self, value):
        """
        Check that the email is unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class PreferenciasSerializer(serializers.ModelSerializer):
    """
    Serializer for the Preferencias model
    """
    class Meta:
        model = Preferencias
        fields = [
            'tema_oscuro',
            'notificaciones_email',
            'notificaciones_push',
            'idioma'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserWithPreferenciasSerializer(serializers.ModelSerializer):
    """
    Serializer that includes user data with their preferences
    """
    preferencias = PreferenciasSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'preferencias'
        ]
        read_only_fields = ['id'] 