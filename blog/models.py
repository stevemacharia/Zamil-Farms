from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    content = models.CharField(max_length=255, null=False, unique=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Blog"

    def __str__(self):
        return f'{self.Title}'
