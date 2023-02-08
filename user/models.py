from django.db import models
import uuid
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, blank=True)
    address_county = models.CharField(max_length=100, blank=True)
    address_city_town = models.CharField(max_length=100, blank=True)
    # phone_number = PhoneNumberField(null=False, blank=True)
    profile_pic = models.ImageField(default='default_profile.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = "User Profile"