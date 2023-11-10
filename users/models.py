from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework_simplejwt.tokens import RefreshToken

from core.models import BaseModel

from users.managers import UserManager


class User(AbstractUser, BaseModel):
    """API User model.

    Attributes
    ----------
    name : CharField
        The users name.
    email : EmailField
        The users email address.
    created_at : DateTimeField
        The timestamp for when the user was created.
    updated_at : DateTimeField
        The timestamp for when the user object was last edited.
    is_removed : BooleanField
        Indicates that a user object has been soft deleted.
    is_email_verified : BooleanField
        Indicates that the users email address has been verified.

    Methods
    -------
    get_auth_tokens ()
        Returns auth tokens for the user.
    """
    username = None
    date_joined = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="Email Verified",
        help_text="Designates whether the users email address has been verified or not.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def get_auth_tokens(self):
        """Returns auth tokens for the user.

        Returns:
            dict: Returns a dictionary containing access_token and refresh_token.
        """
        tokens = RefreshToken.for_user(self)
        return {"refresh_token": str(tokens), "access_token": str(tokens.access_token)}
