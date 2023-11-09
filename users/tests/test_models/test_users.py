from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError

from users.tests.factories import UserFactory

User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.name = "Person Name"
        self.email = "person.name@email.com"
        self.user = UserFactory(name=self.name, email=self.email)

    def test_fields(self):
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.name, self.name)

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.email)

    def test_create_user(self):
        email = "new.person@email.com"
        user = User.objects.create_user(
            name=self.name, email=email, password="longpassword"
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, self.name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_invalid_data(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name="Some Person", email=None, password="longpassword"
            )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                name=self.name, email=self.email, password="longpassword"
            )

    def test_create_superuser(self):
        email = "admin.user@email.com"
        name = "Admin User"
        user = User.objects.create_superuser(
            name=name, email=email, password="longpassword"
        )
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_email_verified)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
