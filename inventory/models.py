from django.db import models
import uuid
from django.utils import timezone


class Medicine(models.Model):
    Product_name = models.CharField(max_length=100)
    purchasing_date = models.DateField()
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    Product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.Product_name

class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # ForeignKey to Medicine
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    order_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_price = self.product.Product_price * self.quantity  # Calculate total price
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.product.Product_name}"

    


class Transaction(models.Model):
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Income: {self.income or 0}, Expense: {self.expense or 0}'