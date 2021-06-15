from rest_framework import status

from .base_test import BaseTestCase


class DiscountProductTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def test_discount_product(self):
        """
        Test discounting a product
        """
        product = self.create_product(self.product, self.admin_user)
        old_discount_price = float(product.discount_price)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            url, data=self.discount_product, format='json')
        new_discount_price = float(response.data['product']['discount_price'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(new_discount_price, old_discount_price)

    def test_discount_price_invalid_request(self):
        """
        Test discounting a product invalid request body
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            url, data=self.invalid_patch, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_discount_product_unauthenticated(self):
        """
        Test discount product when not logged in
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        response = self.client.patch(
            url, data=self.discount_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_discount_product_unauthorized(self):
        """
        Test discount product when not staff
        """
        product = self.create_product(self.product, self.admin_user)

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, data=self.discount_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RemoveDiscountFromProductTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/products/'

    def add_discount_product(self):
        """
        Create dummy product and apply discount
        """
        product = self.create_discount_product(self.product, self.admin_user)

        return product

    def test_remove_product_discount(self):
        product = self.add_discount_product()
        old_discount_price = product.discount_price

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            url, data=self.remove_product_discount, format='json')
        new_discount_price = float(response.data['product']['discount_price'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(new_discount_price, old_discount_price)

    def test_remove_product_discount_invalid_request(self):
        """
        Test removing discount with invalid request body
        """
        product = self.add_discount_product()

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            url, data=self.invalid_patch, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_product_discount_unauthenticated(self):
        """
        Test removing discount with invalid request body
        """
        product = self.add_discount_product()

        url = f'{self.url}{product.id}/'

        response = self.client.patch(
            url, data=self.remove_product_discount, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_product_discount_unauthorized(self):
        """
        Test removing discount with invalid request body
        """
        product = self.add_discount_product()

        url = f'{self.url}{product.id}/'

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, data=self.remove_product_discount, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
