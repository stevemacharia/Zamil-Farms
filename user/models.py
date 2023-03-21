from django.db import models
import uuid
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_county = models.CharField(null=False, max_length=255, blank=True)
    address_city_town = models.CharField(null=False, max_length=255, blank=True)
    phone_number = PhoneNumberField(null=False, blank=True)
    profile_pic = models.ImageField(default='default_profile.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = "User Profile"


class Messages(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Replied', 'Replied'),
    ]
    username = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    message = models.TextField(max_length=500, null=False, blank=False)
    status = models.CharField(choices=STATUS_CHOICES, default='New', max_length=100, blank=True)

    class Meta:
        verbose_name = "Visitor Message"