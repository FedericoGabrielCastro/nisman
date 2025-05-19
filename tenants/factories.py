import factory
from factory.django import DjangoModelFactory
from .models import Tenant


class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant

    name = factory.Faker('company')
    schema_name = factory.Sequence(lambda n: f'schema_{n}')
    domain = factory.Sequence(lambda n: f'tenant{n}.example.com')
    is_active = True 