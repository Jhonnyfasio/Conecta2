# factories.py
import factory
from factory.django import DjangoModelFactory

from .models import User

# Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker("first_name")

# Using a factory with auto-generated data
u = UserFactory()
u.name # Kimberly
u.id # 51