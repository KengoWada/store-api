import factory

from products.models import Product

__all__ = ("ProductFactory",)


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"name {n}")
    description = factory.Sequence(lambda n: f"description {n}")
    price = 1200.00
    quantity = 15
    images = ["https://image.com"]
    is_removed = factory.Faker("boolean", chance_of_getting_true=25)

    class Meta:
        model = Product
