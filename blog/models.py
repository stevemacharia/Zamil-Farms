from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django import forms

# Create your models here.
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(max_length=160)
    content = models.TextField(blank=True, null=False, default="description")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    blog_image = models.ImageField(upload_to='blog_pics', blank=True, null=False,
                                   default='product_pics/zamil_farm_product.png')

    class Meta:
        verbose_name = "Blog"

    def __str__(self):
        return f'{self.title}'

    def save(self):
        super().save()

        img = Image.open(self.blog_image.path)

        if img.height > 850 or img.width > 350:
            output_size = (850, 350)
            img.thumbnail(output_size)
            img.save(self.blog_image.path)
