from http import HTTPStatus

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from products.models import Category
from products.tests.factories import CategoryFactory
from users.tests.factories import UserFactory


class CategoriesCreateListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.user = UserFactory()
        self.url = reverse("categories:category-create-list")

    def test_create_category(self):
        data = {"name": "Category Name", "description": "Category Description"}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "category"])
        self.assertEqual(response_data["message"], "Done")
        category = response_data["category"]
        self.assertEqual(category["name"], data["name"])
        self.assertEqual(category["description"], data["description"])

        self.assertTrue(Category.objects.filter(pk=category["id"]).exists())

    def test_create_category_invalid_data(self):
        data = {"name": "Category Name"}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"]["description"][0], "This field is required."
        )

    def test_create_category_not_authenticated(self):
        data = {"name": "Category Name", "description": "Category Description"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"], "Authentication credentials were not provided."
        )

    def test_create_category_not_staff(self):
        data = {"name": "Category Name", "description": "Category Description"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Permission denied")

    def test_get_categories(self):
        CategoryFactory.create_batch(15)

        # Get categories not staff
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "categories"])
        self.assertEqual(response_data["message"], "Done")

        # Get categories as staff
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "categories"])
        self.assertEqual(response_data["message"], "Done")
        self.assertEqual(len(response_data["categories"]), 15)
