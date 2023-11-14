from rest_framework.test import APITestCase

from products.tests.factories import ProductFactory


class ProductModelTestCase(APITestCase):
    def setUp(self):
        self.name = "Product"
        self.description = "Product description"
        self.price = 4500.00
        self.quantity = 23
        self.images = ["https://localhost:3000"]
        self.product = ProductFactory(
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
            images=self.images,
        )

    def test_fields(self):
        self.assertEqual(self.product.name, self.name)
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertFalse(self.product.is_discounted)
        self.assertCountEqual(self.product.images, self.images)

    def test_string_representation(self):
        string_representation = f"{self.product.pk}: {self.product.name}"
        self.assertEqual(str(self.product), string_representation)
