from django.db import models
from django.utils.translation import gettext_lazy as _

class Tenant(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    schema_name = models.CharField(_('Schema Name'), max_length=63, unique=True)
    domain = models.CharField(_('Domain'), max_length=253, unique=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')
        ordering = ['name']

    def __str__(self):
        return self.name
