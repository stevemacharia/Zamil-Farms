from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Order(models.Model):
    order_name_id = models.CharField(primary_key=True, default=uuid.uuid4, blank=True, editable=False, max_length=100)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_doc = models.FileField(upload_to='invoices', blank=True, null=False)
    date_ordered = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, default="UNPAID")


class OrderDetail(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, blank=True, editable=False, max_length=100)
    order_name = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_quantity = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)


