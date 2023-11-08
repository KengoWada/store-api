import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

__all__ = ("UserFactory",)

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    name = factory.Sequence(lambda n: f"name {n}")
    password = make_password("longpassword")

    class Meta:
        model = User