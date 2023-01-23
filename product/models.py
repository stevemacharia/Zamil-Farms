from django.db import models
from PIL import Image
from django.utils import timezone
import uuid

# Create your models here.
# Create your models here.
class Product(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, blank=True, editable=False, max_length=100)
    name = models.CharField(max_length=255, null=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='product_pics', blank=True, null=False, default='product_pics/zamil_farm_product.png')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def delete(self, *args, **kwargs):
        if self.image != 'product_pics/zamil_farm_product.png':
            self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Product"

    def __str__(self):
        return f'{self.name}'
