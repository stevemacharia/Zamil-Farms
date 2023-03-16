from django.db import models
from PIL import Image
from django.utils import timezone
import uuid


class ProductCategory(models.Model):
    product_category_id = models.CharField(primary_key=True, default=uuid.uuid4, blank=True, editable=False,
                                           max_length=100)
    category_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f'{self.category_name} Category'

    class Meta:
        verbose_name = "Product Categories"


# Create your models here.
class Product(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, blank=True, editable=False, max_length=100)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True, )
    product_name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    date_created = models.DateTimeField(default=timezone.now)
    main_image = models.ImageField(upload_to='product_pics', blank=True, null=False,
                                   default='product_pics/zamil_farm_product.png')
    product_description = models.CharField(null=False, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.main_image.path)
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.main_image.path)

    def delete(self, *args, **kwargs):
        if self.main_image != 'product_pics/zamil_farm_product.png':
            self.main_image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Product"

    def __str__(self):
        return f'{self.product_name}'


class ProductImage(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_pics', default='default.jpg')

    def __str__(self):
        return f'{self.product.product_name} Product image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 900 or img.width > 900:
            output_size = (900, 900)
            img.thumbnail(output_size)
            img.save(self.image.path)
