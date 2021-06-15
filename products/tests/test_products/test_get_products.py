from rest_framework import status

from .base_test import BaseTestCase


class GetProductsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def add_products(self):
        """
        Create dummy products
        """
        self.create_product(self.product, self.admin_user)
        self.create_product(self.other_product, self.admin_user)

    def test_get_products(self):
        """
        Test getting products
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.add_products()
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 2)


class GetProuctTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def add_product(self):
        """
        Create dummy product
        """
        return self.create_product(self.product, self.admin_user)

    def test_get_product(self):
        """
        Test getting products
        """
        product = self.add_product()
        url = f'{self.url}{product.id}/'

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_deleted_product(self):
        """
        Test getting a product that has been soft-deleted
        """
        product = self.add_product()
        product.is_deleted = True
        product.save()

        url = f'{self.url}{product.id}/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
