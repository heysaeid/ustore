from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return str(self.username)