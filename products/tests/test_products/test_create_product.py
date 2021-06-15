from rest_framework import status

from .base_test import BaseTestCase


class CreateProductTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def test_create_product(self):
        """
        Test creating a product
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url, data=self.product, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_invalid_request(self):
        """
        Test creating a product with an invalid body
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            self.url, data=self.invalid_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.url, data=self.invalid_other_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_unauthenticated(self):
        """
        Test creating a product when not authenticated
        """
        response = self.client.post(self.url, data=self.product, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_unauthorized(self):
        """
        Test creating a product when not staff member
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.product, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
