from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import BaseModel


class Product(BaseModel):
    """Product model."""

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(
        max_digits=11, decimal_places=2, null=False, blank=False
    )
    discount_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    quantity = models.IntegerField(null=False, blank=False)
    images = ArrayField(
        models.URLField(null=False, blank=False), null=False, blank=False
    )

    class Meta:
        db_table = "products"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.pk}: {self.name}"

    @property
    def is_discounted(self):
        return self.discount_price > 0
