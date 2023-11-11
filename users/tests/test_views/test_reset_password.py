from http import HTTPStatus

from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.utils import generate_token

from users.tests.factories import UserFactory


class ResetPasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_email_verified=True)
        self.url = reverse("reset-password")

    def assign_user_password_reset_token(self):
        token = generate_token(self.user.email)
        self.user.password_reset_token = token
        self.user.save(update_fields=["password_reset_token"])
        return token

    def test_reset_password(self):
        data = {
            "token": self.assign_user_password_reset_token(),
            "password": "l0ngPassword@",
        }
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "Done")
        self.assertIsNotNone(
            authenticate(email=self.user.email, password=data["password"])
        )

    def test_reset_password_invalid_request(self):
        # Test invalid token
        data = {"token": "wrong_token", "password": "l0ngPassword@"}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid token")
        self.assertIsNone(authenticate(email=self.user.email, password="l0ngPassword@"))

        # Test invalid password
        data = {"token": self.assign_user_password_reset_token(), "password": "short"}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        password_error = response_data["error"]["password"][0]
        self.assertEqual(password_error, "Password must be at least 8 characters long.")
        self.assertIsNone(authenticate(email=self.user.email, password="short"))


class ForgotPasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("forgot-password")

    def test_forgot_password(self):
        self.assertFalse(self.user.password_reset_token)

        data = {"email": self.user.email}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "Done")

        self.user.refresh_from_db()
        self.assertTrue(self.user.password_reset_token)

    def test_forgot_password_invalid_email(self):
        self.assertFalse(self.user.password_reset_token)

        data = {"email": "fake@email.com"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "Done")

        self.user.refresh_from_db()
        self.assertFalse(self.user.password_reset_token)
