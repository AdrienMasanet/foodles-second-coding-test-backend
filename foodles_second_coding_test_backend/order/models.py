import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from client.models import Client
from product.models import Product


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"
        CANCELLED = "CANCELLED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderProduct")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.email + " - " + self.status + " - " + str(self.total_price) + "€"


@receiver(post_save, sender=Order)
# Calculate total price of order automatically when order is saved
def calculate_total_price(sender, instance, **kwargs):
    total_price = 0
    # Get all order products objects for this order and calculate the total price, select related product to avoid N+1 queries
    for order_product in instance.orderproduct_set.select_related("product").all():
        total_price += order_product.product.price * order_product.quantity
    instance.total_price = total_price


# This model below is used to store the quantity of each product in an order
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
