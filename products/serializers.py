from rest_framework import serializers

from products.models import Category, Product


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
            "category",
        )
        extra_kwargs = {"category": {"required": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.category:
            data["category"] = (
                instance.category.name if not instance.category.is_removed else None
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")
        extra_kwargs = {"description": {"required": True}}
