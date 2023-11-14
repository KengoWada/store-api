from django.contrib import admin

from core.admin import BaseModelAdmin

from products.models import Product

__all__ = ("ProductModelAdmin",)


@admin.register(Product)
class ProductModelAdmin(BaseModelAdmin):
    readonly_fields = ("is_discounted", *BaseModelAdmin.READONLY_FIELDS)
    fieldsets = (
        (None, {"fields": ("name", "description")}),
        (
            "Details",
            {
                "fields": (
                    "price",
                    "discount_price",
                    "is_discounted",
                    "quantity",
                    "images",
                )
            },
        ),
        ("Misc", {"fields": ("is_removed", "created_at", "updated_at")}),
    )

    list_display = ("name", "price", "quantity")
    list_filter = ("is_removed",)

    search_fields = ("name", "description")
    ordering = ("price", "quantity")
