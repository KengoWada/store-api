from django.contrib.postgres.fields import ArrayField
from django.db import models

STOCK_ACTIONS = [
    ('create_product', 'Create a new product'),
    ('update_product_details', 'Update product details'),
    ('delete_product', 'Delete a product'),
    ('add_stock', 'Increment the current stock of a product'),
    ('remove_stock', 'Decrement the current stock of a product'),
    ('discount_product', 'Add a discount to a product'),
    ('remove_discount', 'Remove discount from a product'),
]


class Product(models.Model):

    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    images = ArrayField(models.URLField(), null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    @property
    def is_discounted(self):
        return self.discount_price > 0


class StockRecord(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', null=False,
                             on_delete=models.DO_NOTHING)
    action = models.CharField(choices=STOCK_ACTIONS,
                              max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_records'


# class Review(models.Model):
#     user = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     product = models.ForeignKey('Products', on_delete=models.CASCADE)
#     review = models.TextField()
#     rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'product_reviews'
