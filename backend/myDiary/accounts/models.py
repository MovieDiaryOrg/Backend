from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionManager

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username
    