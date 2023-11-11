import re

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        if not re.match(r"(?=(?:[^A-Z]*[A-Z]){1})", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 upper case character."
            )

        if not re.match(r"(?=(?:[^a-z]*[a-z]){1})", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 lower case character."
            )

        if not re.match(r"(?=(?:\D*\d){1})", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 number."
            )

        if not re.sub(r"[a-zA-Z0-9]", "", value):
            raise serializers.ValidationError(
                "Password must contain at least 1 special character."
            )

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        if password:
            instance.password_reset_token = ""
            instance.set_password(password)
            validated_data.pop("password")

        return super().update(instance, validated_data)
