from rest_framework import status


from .base_test import BaseTestCase


class SoftDeleteProduct(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def test_soft_delete_product(self):
        """
        Test deleting a product
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_soft_delete_product_invalid_id(self):
        """
        Test deleting a product with an invalid id
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}0/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_product_unauthenticated(self):
        """
        Test deleting a product when not logged in
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_soft_delete_product_unauthorized(self):
        """
        Test deleting a product when not staff
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
