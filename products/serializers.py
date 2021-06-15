from rest_framework import serializers

from .models import Product, StockRecord


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discount_price',
                  'quantity', 'images', 'rating', 'is_deleted')


class GetProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'discount_price',
                  'quantity', 'images', 'rating', 'is_discounted')


class StockRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockRecord
        fields = ('user', 'product', 'action')

    user = serializers.ReadOnlyField()
    product = serializers.ReadOnlyField()
