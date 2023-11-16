from http import HTTPStatus

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from products.tests.factories import CategoryFactory
from users.tests.factories import UserFactory


class CategoryDetailsUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.staff_user = UserFactory(is_staff=True)
        self.category = CategoryFactory(is_removed=False)
        self.removed_category = CategoryFactory(is_removed=True)
        self.url = reverse(
            "categories:category-details-update", args=[self.category.pk]
        )
        self.removed_url = reverse(
            "categories:category-details-update", args=[self.removed_category.pk]
        )

    def test_get_category_details(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "category"])
        self.assertEqual(response_data["message"], "Done")
        category = response_data["category"]
        self.assertEqual(category["name"], self.category.name)
        self.assertEqual(category["description"], self.category.description)

    def test_get_category_details_removed_id(self):
        response = self.client.get(self.removed_url, format="json")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid category id.")

    def test_update_category_details(self):
        data = {"name": "New Category Name"}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message", "category"])
        self.assertEqual(response_data["message"], "Done")

        self.category.refresh_from_db()
        category = response_data["category"]
        self.assertEqual(category["name"], self.category.name)
        self.assertEqual(category["description"], self.category.description)

    def test_update_category_details_invalid_data(self):
        data = {"name": None}
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"]["name"][0], "This field may not be null."
        )

    def test_update_category_details_invalid_id(self):
        data = {"name": "New Category Name"}
        url = reverse("categories:category-details-update", args=[0])
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid category id.")

    def test_update_category_details_not_authenticated(self):
        data = {"name": "New Category Name"}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"], "Authentication credentials were not provided."
        )

    def test_update_category_details_not_staff(self):
        data = {"name": "New Category Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Permission denied")
