from rest_framework import serializers
from rest_framework.test import APITestCase


from users.models import User
from products.models import Product
from products.serializers import ProductSerializer, StockRecordSerializer


class BaseTestCase(APITestCase):

    def setUp(self):
        # Create dummy users
        self.user = User.objects.create_user(
            email='some@email.com', password='complex_password')
        self.admin_user = User.objects.create_superuser(
            email='admin@email.com', password='complex_password')

        # Create dummy product data
        self.images = ['https://localhost:3000/image']

        self.product = {'name': 'SomeThing', 'description': 'Something description',
                        'price': 2000, 'quantity': 20, 'images': self.images}
        self.other_product = {'name': 'OtherThing', 'description': 'other thing description',
                              'price': 1000, 'quantity': 5, 'images': self.images}

        # Invalid values
        self.invalid_images = ['something_useless']
        self.invalid_product = {'name': 'SomeThing', 'description': 'Something description',
                                'price': 2000}
        self.invalid_other_product = {'name': 'OtherThing', 'description': 'other thing description',
                                      'price': 1000, 'quantity': 5, 'images': self.invalid_images}
        self.invalid_update_product = {'quantity': 12}
        self.invalid_patch = {}

        # Update data
        self.update_product = {'name': 'New SomeThing',
                               'description': 'New something description'}
        self.update_other_product = {
            'name': 'New OtherThing', 'description': 'New OtherThing description'}

        # PATCH actions
        self.discount_product = {'discount_product': {'discount_price': 800}}
        self.remove_product_discount = {'remove_product_discount': ''}
        self.add_product_stock = {'add_product_stock': {'increment_by': 3}}
        self.remove_product_stock = {
            'remove_product_stock': {'decrement_by': 2}}

    def create_product(self, data, user):
        """
        Create a dummy product
        """
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        data = {'action': 'create_product'}
        stock_record_serializer = StockRecordSerializer(data=data)
        if stock_record_serializer.is_valid():
            stock_record_serializer.save(
                user=user, product=serializer.instance)

        return serializer.instance

    def create_discount_product(self, data, user):
        """
        Discount a product
        """
        product = self.create_product(data, user)

        serializer = ProductSerializer(
            product, data=self.discount_product['discount_product'], partial=True)
        if serializer.is_valid():
            serializer.save()

        data = {'action': 'discount_product'}
        stock_reccord_serializer = StockRecordSerializer(data=data)
        if stock_reccord_serializer.is_valid():
            stock_reccord_serializer.save(
                user=user, product=product)

        return serializer.instance
