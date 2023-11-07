from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    Base model for all models in the app.

    Attributes
    ----------
    created_at : DateTimeField
        The timestamp for when the object was created.
    updated_at : DateTimeField
        The timestamp for when the object was updated.
    is_removed : boolean
        Indicates that an object has been deleted(soft delete).
    history    : HistoricalRecords
        Track objects create, update and delete.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(
        default=False,
        verbose_name="Removed",
        help_text="Designates that this object has been soft deleted.",
    )
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
