from django.db import models
import uuid
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=True)
    age = models.IntegerField(default=0, null=False)
    profile_pic = models.ImageField(default='default_profile.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = "User Profile"