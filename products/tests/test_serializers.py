from rest_framework.test import APITestCase

from products.serializers import ProductSerializer
from products.tests.factories import ProductFactory


class ProductSerializerTestCase(APITestCase):
    def setUp(self):
        self.product = ProductFactory()

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
