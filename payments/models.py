from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MpesaTransaction(models.Model):
    timeStamp = models.DateTimeField(default=timezone.now)
    order_name_id = models.CharField(max_length=100, blank=True, null=True)
    # customer_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'Order: {self.order_name_id}'

    class Meta:
        verbose_name = 'Mpesa Transaction'
        verbose_name_plural = 'Mpesa Transactions'
