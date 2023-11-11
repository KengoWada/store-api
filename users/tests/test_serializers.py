from rest_framework.test import APITestCase

from users.serializers import UserSerializer
from users.tests.factories import UserFactory


class UserSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_serializer_fields(self):
        serializer = UserSerializer(self.user)
        user_data = serializer.data
        serializer_fields = [
            key for key, value in serializer.fields.items() if not value.write_only
        ]
        self.assertCountEqual(user_data.keys(), serializer_fields)
        self.assertEqual(user_data["id"], self.user.pk)
        self.assertEqual(user_data["name"], self.user.name)
        self.assertEqual(user_data["email"], self.user.email)

    def test_serializer_create(self):
        data = {
            "email": "new.person@email.com",
            "name": "New Person",
            "password": "l0ngP@ssword",
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        self.assertFalse(serializer.errors)
        serializer.save()

        user = serializer.instance
        self.assertEqual(user.name, data["name"])
        self.assertEqual(user.email, data["email"])
        self.assertIn("argon2", user.password)

    def test_serializer_update(self):
        data = {"name": "New Name"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        self.assertFalse(serializer.errors)
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])

    def test_serializer_validate_password(self):
        data = {"password": "short"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must be at least 8 characters long."
        self.assertEqual(serializer.errors["password"][0], error_message)

        data = {"password": "shortpassword"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must contain at least 1 upper case character."
        self.assertEqual(serializer.errors["password"][0], error_message)

        data = {"password": "SHORTPASSWORD"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must contain at least 1 lower case character."
        self.assertEqual(serializer.errors["password"][0], error_message)

        data = {"password": "SHORTpassword"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must contain at least 1 number."
        self.assertEqual(serializer.errors["password"][0], error_message)

        data = {"password": "SH0RTpassw0rd"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must contain at least 1 special character."
        self.assertEqual(serializer.errors["password"][0], error_message)

        data = {"password": "SH0RTp@ssw0rd!"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        serializer.is_valid()
        error_message = "Password must contain at least 1 special character."
        self.assertFalse(serializer.errors)
