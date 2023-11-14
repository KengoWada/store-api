from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    is_discounted = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "discount_price",
            "quantity",
            "images",
            "is_discounted",
        )
