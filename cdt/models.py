from django.db import models
from django.contrib.auth.models import User

"""
// TypeScript Interface equivalente:
interface User {
    id: number;
    username: string;
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    is_active: boolean;
    is_staff: boolean;
    is_superuser: boolean;
    date_joined: Date;
    last_login: Date;
}

interface Preferencias {
    id: number;
    user: User;  // Relación OneToOne con User
    tema_oscuro: boolean;
    notificaciones_email: boolean;
    notificaciones_push: boolean;
    idioma: string;
    created_at: Date;
    updated_at: Date;
}
"""

# Create your models here.

class Preferencias(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferencias')
    tema_oscuro = models.BooleanField(default=False)
    notificaciones_email = models.BooleanField(default=True)
    notificaciones_push = models.BooleanField(default=True)
    idioma = models.CharField(max_length=10, default='es')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Preferencia'
        verbose_name_plural = 'Preferencias'

    def __str__(self):
        return f'Preferencias de {self.user.username}'
