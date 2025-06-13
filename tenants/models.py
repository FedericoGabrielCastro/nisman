from django.db import models
from django.utils.translation import gettext_lazy as _


class TenantQuerySet(models.QuerySet):
    # Aquí puedes agregar métodos custom, por ejemplo:
    def activos(self):
        return self.filter(is_active=True)

    def with_name(self, name):
        return self.filter(name__icontains=name)


class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)


class Tenant(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    schema_name = models.CharField(
        _('Schema Name'), max_length=63, unique=True
    )
    domain = models.CharField(_('Domain'), max_length=253, unique=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    objects = TenantManager()

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')
        ordering = ['name']

    def __str__(self):
        return self.name
