from rest_framework.test import APITestCase

from products.tests.factories import CategoryFactory, ProductFactory


class ProductModelTestCase(APITestCase):
    def setUp(self):
        self.name = "Product"
        self.description = "Product description"
        self.price = 4500.00
        self.quantity = 23
        self.images = ["https://localhost:3000"]
        self.category = CategoryFactory()
        self.product = ProductFactory(
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
            images=self.images,
            category=self.category,
        )

    def test_fields(self):
        self.assertEqual(self.product.name, self.name)
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertFalse(self.product.is_discounted)
        self.assertCountEqual(self.product.images, self.images)
        self.assertEqual(self.product.category.pk, self.category.pk)

    def test_string_representation(self):
        string_representation = f"{self.product.pk}: {self.product.name}"
        self.assertEqual(str(self.product), string_representation)


class CategoryModelTestCase(APITestCase):
    def setUp(self):
        self.name = "Category Name"
        self.description = "Category Description"
        self.category = CategoryFactory(
            name=self.name, description=self.description, is_removed=False
        )

    def test_fields(self):
        self.assertEqual(self.category.name, self.name)
        self.assertEqual(self.category.description, self.description)
        self.assertFalse(self.category.is_removed)

    def test_string_representation(self):
        self.assertEqual(str(self.category), self.name)
