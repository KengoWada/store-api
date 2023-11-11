from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from core.admin import BaseModelAdmin

from users.models import User

__all__ = ("UserModelAdmin",)


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


@admin.register(User)
class UserModelAdmin(UserAdmin, BaseModelAdmin):
    readonly_fields = ("password_reset_token", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "email", "password", "password_reset_token")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_email_verified",
                    "is_staff",
                    "is_superuser",
                    "is_removed",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("created_at", "updated_at", "last_login")}),
    )

    add_form = UserCreationForm
    add_fieldsets = (
        (None, {"fields": ("email", "name", "password1", "password2")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_email_verified",
                    "is_staff",
                    "is_superuser",
                    "is_removed",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    list_display = (
        "email",
        "name",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_removed",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_email_verified",
        "is_removed",
    )

    search_fields = ("email", "name")
    ordering = ("email", "name")
