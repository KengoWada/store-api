from rest_framework import status

from .base_test import BaseTestCase


class UpdateProductTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def test_update_product(self):
        """
        Test updating a product
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(
            url, data=self.update_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_invalid_request(self):
        """
        Test updating a product with invalid request body
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(
            url, data=self.invalid_update_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_invalid_id(self):
        """
        Test updating an invalid product
        """
        url = f'{self.url}0/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(
            url, data=self.invalid_update_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_unauthenticated(self):
        """
        Test updating a product when not logged in
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        response = self.client.put(
            url, data=self.invalid_update_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product_unauthorized(self):
        """
        Test updating a product when not staff
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            url, data=self.invalid_update_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
