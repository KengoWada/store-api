from http import HTTPStatus

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from products.serializers import ProductSerializer
from products.tests.factories import ProductFactory
from users.tests.factories import UserFactory


class ProductDetailsUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.product = ProductFactory(is_removed=False)
        self.removed_product = ProductFactory(is_removed=True)
        self.url = reverse("products:product-details-update", args=[self.product.pk])
        self.removed_url = reverse(
            "products:product-details-update", args=[self.removed_product.pk]
        )

    def test_get_product_details(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "product"])
        self.assertEqual(response_data["message"], "Done")

        product = response_data["product"]
        self.assertCountEqual(product.keys(), ProductSerializer.Meta.fields)
        self.assertEqual(product["id"], self.product.pk)
        self.assertEqual(product["name"], self.product.name)
        self.assertEqual(product["description"], self.product.description)
        self.assertEqual(product["price"], f"{self.product.price:.2f}")
        self.assertEqual(
            product["discount_price"], f"{self.product.discount_price:.2f}"
        )
        self.assertEqual(product["quantity"], self.product.quantity)
        self.assertCountEqual(product["images"], self.product.images)
        self.assertFalse(product["is_discounted"])

    def test_get_product_details_invalid_id(self):
        # Test getting prouct with wrong id.
        url = reverse("products:product-details-update", args=[0])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid product id.")

        # Test getting product with is_removed=True
        response = self.client.get(self.removed_url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid product id.")

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.removed_url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "product"])
        self.assertEqual(response_data["message"], "Done")

        product = response_data["product"]
        self.assertCountEqual(product.keys(), ProductSerializer.Meta.fields)
        self.assertEqual(product["id"], self.removed_product.pk)
        self.assertEqual(product["name"], self.removed_product.name)
        self.assertEqual(product["description"], self.removed_product.description)
        self.assertEqual(product["price"], f"{self.removed_product.price:.2f}")
        self.assertEqual(
            product["discount_price"], f"{self.removed_product.discount_price:.2f}"
        )
        self.assertEqual(product["quantity"], self.removed_product.quantity)
        self.assertCountEqual(product["images"], self.removed_product.images)
        self.assertFalse(product["is_discounted"])

    def test_update_product_details(self):
        data = {"name": "Update Product Name", "discount_price": "950.00"}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "product"])
        self.assertEqual(response_data["message"], "Done")

        self.product.refresh_from_db()

        product = response_data["product"]
        self.assertEqual(product["name"], self.product.name)
        self.assertEqual(
            product["discount_price"], f"{self.product.discount_price:.2f}"
        )
        self.assertTrue(product["is_discounted"])

    def test_update_product_details_invalid_data(self):
        data = {"name": "New Product Name", "price": False}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"]["price"][0], "A valid number is required."
        )

        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, data["name"])

    def test_update_product_details_invalid_id(self):
        data = {"name": "Update Product Name", "discount_price": "950.00"}
        url = reverse("products:product-details-update", args=[0])
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid product id.")

        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, data["name"])

    def test_update_product_details_not_authenticated(self):
        data = {"name": "Update Product Name", "discount_price": "950.00"}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"], "Authentication credentials were not provided."
        )

    def test_update_product_details_not_staff(self):
        data = {"name": "Update Product Name", "discount_price": "950.00"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Permission denied")
