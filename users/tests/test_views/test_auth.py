from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory

User = get_user_model()


class RegisterUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth:register-user")

    def test_register_user(self):
        data = {
            "email": "first.person@email.com",
            "name": "First Person",
            "password": "l0ngPassword@",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "Done")
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_register_user_invalid_request(self):
        data = {"name": "First Person", "password": "l0ngPassword@"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertCountEqual(response_data["error"].keys(), ["email"])
        email_error = response_data["error"]["email"][0]
        self.assertEqual(email_error, "This field is required.")


class LoginUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_email_verified=True)
        self.user_2 = UserFactory()
        self.user_3 = UserFactory(is_active=False)
        self.url = reverse("auth:login-user")

    def test_login_user(self):
        data = {"email": self.user.email, "password": "longpassword"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(
            response_data.keys(), ["message", "user", "refresh_token", "access_token"]
        )

    def test_login_user_invalid_request(self):
        data = {"email": "fake@email.com", "password": "longpassword"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid credentials")

    def test_login_user_email_not_verified(self):
        data = {"email": self.user_2.email, "password": "longpassword"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(
            response_data["error"], "Please verify your email address to continue."
        )

    def test_login_user_not_active(self):
        data = {"email": self.user_3.email, "password": "longpassword"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid credentials")
