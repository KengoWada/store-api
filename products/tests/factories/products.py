import factory

from products.models import Category, Product

__all__ = ("ProductFactory", "CategoryFactory")


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"name {n}")
    description = factory.Sequence(lambda n: f"description {n}")
    price = 1200.00
    quantity = 15
    images = ["https://image.com"]
    is_removed = factory.Faker("boolean", chance_of_getting_true=25)
    category = factory.SubFactory("products.tests.factories.products.CategoryFactory")

    class Meta:
        model = Product


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"category name {n}")
    description = factory.Sequence(lambda n: f"category description {n}")
    is_removed = factory.Faker("boolean", chance_of_getting_true=25)

    class Meta:
        model = Category
