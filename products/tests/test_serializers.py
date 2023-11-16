from rest_framework.test import APITestCase

from products.models import Product
from products.serializers import ProductSerializer
from products.tests.factories import CategoryFactory, ProductFactory


class ProductSerializerTestCase(APITestCase):
    def setUp(self):
        self.category = CategoryFactory(is_removed=False)
        self.product = ProductFactory(category=self.category)

    def test_fields(self):
        serializer = ProductSerializer(self.product)
        serializer_fields = [
            key for key, value in serializer.fields.items() if not value.write_only
        ]
        self.assertCountEqual(serializer.data.keys(), serializer_fields)
        self.assertEqual(serializer.data["id"], self.product.id)
        self.assertEqual(serializer.data["name"], self.product.name)
        self.assertEqual(serializer.data["description"], self.product.description)
        self.assertEqual(serializer.data["price"], f"{self.product.price:.2f}")
        self.assertEqual(
            serializer.data["discount_price"], f"{self.product.discount_price:.2f}"
        )
        self.assertFalse(serializer.data["is_discounted"])
        self.assertEqual(serializer.data["category"], self.category.name)

    def test_create_product(self):
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": "1200.00",
            "quantity": 23,
            "images": ["https://localhost:3000/image.webp"],
            "category": self.category.pk,
        }
        serializer = ProductSerializer(data=data)
        serializer.is_valid()
        self.assertFalse(serializer.errors)
        serializer.save()

        self.assertTrue(Product.objects.filter(pk=serializer.data["id"]).exists())
