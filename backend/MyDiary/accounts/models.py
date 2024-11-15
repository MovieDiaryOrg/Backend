from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    userId = models.TextField()
    name = models.CharField(max_length=30)
    