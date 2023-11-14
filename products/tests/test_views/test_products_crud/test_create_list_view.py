from http import HTTPStatus

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from products.tests.factories import ProductFactory
from users.tests.factories import UserFactory


class ProductCreateListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.url = reverse("products:products-create-list")

    def test_create_product(self):
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": 1200.00,
            "quantity": 23,
            "images": ["https://localhost:3000/image.png"],
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "product"])
        self.assertEqual(response_data["message"], "Done")
        self.assertEqual(response_data["product"]["name"], data["name"])
        self.assertEqual(response_data["product"]["description"], data["description"])
        self.assertEqual(response_data["product"]["price"], f"{data['price']:.2f}")
        self.assertEqual(response_data["product"]["quantity"], data["quantity"])
        self.assertEqual(response_data["product"]["images"], data["images"])

    def test_create_product_invalid_data(self):
        data = {
            "description": "Product description",
            "price": 1200.00,
            "quantity": 23,
            "images": ["https://localhost:3000/image.png"],
        }
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"]["name"][0], "This field is required.")

    def test_create_product_not_authenticated(self):
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": 1200.00,
            "quantity": 23,
            "images": ["https://localhost:3000/image.png"],
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"], "Authentication credentials were not provided."
        )

    def test_create_product_not_staff_member(self):
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": 1200.00,
            "quantity": 23,
            "images": ["https://localhost:3000/image.png"],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Permission denied")

    def test_get_products(self):
        ProductFactory.create_batch(100)

        url = f"{self.url}?p=2&page_size=15"

        # Test fetching products as non staff
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(
            response_data.keys(), ["next", "previous", "count", "results"]
        )
        self.assertEqual(
            response_data["next"], "http://testserver/products/?p=3&page_size=15"
        )
        self.assertEqual(
            response_data["previous"], "http://testserver/products/?page_size=15"
        )
        self.assertEqual(len(response_data["results"]), 15)

        # Test fetching products as staff
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(
            response_data.keys(), ["next", "previous", "count", "results"]
        )
        self.assertEqual(
            response_data["next"], "http://testserver/products/?p=3&page_size=15"
        )
        self.assertEqual(
            response_data["previous"], "http://testserver/products/?page_size=15"
        )
        self.assertEqual(response_data["count"], 100)
        self.assertEqual(len(response_data["results"]), 15)
