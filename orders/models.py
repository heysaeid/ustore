from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from shop.models import Product

User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, blank=True)
    transaction_id = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    final_price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity