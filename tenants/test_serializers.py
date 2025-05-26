from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Tenant
from .serializers import TenantSerializer


class TenantSerializerTest(TestCase):
    def setUp(self):
        self.tenant_data = {
            'name': 'Test Company',
            'schema_name': 'test_company',
            'domain': 'test.example.com',
            'is_active': True
        }
        self.tenant = Tenant.objects.create(**self.tenant_data)
        self.serializer = TenantSerializer(instance=self.tenant)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {
            'id', 'name', 'schema_name', 'domain',
            'is_active', 'created_at', 'updated_at'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_read_only_fields(self):
        """Test that read-only fields cannot be modified"""
        data = {
            'name': 'New Company',
            'schema_name': 'new_company',
            'domain': 'new.example.com',
            'is_active': True,
            'id': 999,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z'
        }
        serializer = TenantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tenant = serializer.save()
        self.assertNotEqual(tenant.id, 999)
        self.assertNotEqual(
            tenant.created_at.isoformat(),
            '2024-01-01T00:00:00Z'
        )

    def test_create_tenant(self):
        """Test creating a new tenant"""
        data = {
            'name': 'New Company',
            'schema_name': 'new_company',
            'domain': 'new.example.com',
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tenant = serializer.save()
        self.assertEqual(tenant.name, 'New Company')
        self.assertEqual(tenant.schema_name, 'new_company')
        self.assertEqual(tenant.domain, 'new.example.com')
        self.assertTrue(tenant.is_active)

    def test_update_tenant(self):
        """Test updating an existing tenant"""
        data = {
            'name': 'Updated Company',
            'is_active': False
        }
        serializer = TenantSerializer(
            instance=self.tenant,
            data=data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        tenant = serializer.save()
        self.assertEqual(tenant.name, 'Updated Company')
        self.assertEqual(tenant.schema_name, 'test_company')
        self.assertFalse(tenant.is_active)

    def test_validation_schema_name(self):
        """Test schema_name validation"""
        # Create a tenant with the schema_name we want to test
        Tenant.objects.create(
            name='First Company',
            schema_name='test_schema',
            domain='first.example.com'
        )
        # Try to create another tenant with the same schema_name
        data = {
            'name': 'Second Company',
            'schema_name': 'test_schema',
            'domain': 'second.example.com',
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('schema_name', serializer.errors)

    def test_validation_domain(self):
        """Test domain validation"""
        # Create a tenant with the domain we want to test
        Tenant.objects.create(
            name='First Company',
            schema_name='first_schema',
            domain='first.example.com'
        )
        # Try to create another tenant with the same domain
        data = {
            'name': 'Second Company',
            'schema_name': 'second_schema',
            'domain': 'first.example.com',  # Same domain as first tenant
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('domain', serializer.errors)

    def test_unique_schema_name(self):
        """Test that schema_name must be unique"""
        # Create first tenant
        Tenant.objects.create(
            name='First Company',
            schema_name='test_schema',
            domain='first.example.com'
        )
        # Try to create second tenant with same schema_name
        data = {
            'name': 'Second Company',
            'schema_name': 'test_schema',  # Same schema_name
            'domain': 'second.example.com',
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('schema_name', serializer.errors)

    def test_unique_domain(self):
        """Test that domain must be unique"""
        # Create first tenant with a different domain
        Tenant.objects.create(
            name='First Company',
            schema_name='first_schema',
            domain='first.example.com'
        )
        # Try to create second tenant with same domain as the one in setUp
        data = {
            'name': 'Second Company',
            'schema_name': 'second_schema',
            'domain': 'test.example.com',  # Same domain as setUp tenant
            'is_active': True
        }
        serializer = TenantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('domain', serializer.errors)

    def test_serialize_multiple_tenants(self):
        """Test serializing multiple tenants"""
        # Create additional tenant
        Tenant.objects.create(
            name='Another Company',
            schema_name='another_company',
            domain='another.example.com'
        )
        tenants = Tenant.objects.all().order_by('id')
        serializer = TenantSerializer(tenants, many=True)
        self.assertEqual(len(serializer.data), 2)
        # Check first tenant (from setUp)
        self.assertEqual(
            serializer.data[0]['name'],
            'Test Company'
        )
        # Check second tenant (newly created)
        self.assertEqual(
            serializer.data[1]['name'],
            'Another Company'
        ) 