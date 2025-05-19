from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Tenant
from .factories import TenantFactory


class TenantModelTest(TestCase):
    def setUp(self):
        self.tenant = TenantFactory()

    def test_tenant_creation(self):
        """Test that a tenant can be created with valid data"""
        self.assertIsInstance(self.tenant, Tenant)
        self.assertTrue(self.tenant.is_active)
        self.assertTrue(len(self.tenant.name) > 0)
        self.assertTrue(len(self.tenant.schema_name) > 0)
        self.assertTrue(len(self.tenant.domain) > 0)

    def test_tenant_str_method(self):
        """Test the string representation of a tenant"""
        self.assertEqual(str(self.tenant), self.tenant.name)

    def test_unique_schema_name(self):
        """Test that schema_name must be unique"""
        with self.assertRaises(Exception):
            TenantFactory(schema_name=self.tenant.schema_name)

    def test_unique_domain(self):
        """Test that domain must be unique"""
        with self.assertRaises(Exception):
            TenantFactory(domain=self.tenant.domain)

    def test_schema_name_max_length(self):
        """Test that schema_name cannot exceed 63 characters"""
        tenant = TenantFactory.build(schema_name='a' * 64)
        with self.assertRaises(ValidationError):
            tenant.full_clean() 