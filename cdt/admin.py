from django.contrib import admin
from .models import Preferencias

@admin.register(Preferencias)
class PreferenciasAdmin(admin.ModelAdmin):
    list_display = ('user', 'tema_oscuro', 'notificaciones_email', 'notificaciones_push', 'idioma', 'updated_at')
    list_filter = ('tema_oscuro', 'notificaciones_email', 'notificaciones_push', 'idioma')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Preferencias', {
            'fields': ('tema_oscuro', 'notificaciones_email', 'notificaciones_push', 'idioma')
        }),
        ('Información Temporal', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
