import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import Preferencias


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class PreferenciasFactory(DjangoModelFactory):
    class Meta:
        model = Preferencias

    user = factory.SubFactory(UserFactory)
    tema_oscuro = False
    notificaciones_email = True
    notificaciones_push = True
    idioma = 'es' 