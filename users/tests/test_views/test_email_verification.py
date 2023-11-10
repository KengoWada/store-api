from http import HTTPStatus

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.utils import generate_token

from users.tests.factories import UserFactory


class VerifyEmailAddressAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("verify-email-address")

    def test_verify_email_address(self):
        self.assertFalse(self.user.is_email_verified)

        data = {"token": generate_token(self.user.email)}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "Done")

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_verify_email_address_invalid_token(self):
        data = {"token": "RandomInvalidToken"}
        response = self.client.patch(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["error"])
        self.assertEqual(response_data["error"], "Invalid token.")


class ResendEmailAddressVerificationEmailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("resend-email-verification-email")

    def test_resend_email_address_verification_email(self):
        data = {"email": self.user.email}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertCountEqual(response_data.keys(), ["message"])
        self.assertEqual(response_data["message"], "An email has been sent.")
