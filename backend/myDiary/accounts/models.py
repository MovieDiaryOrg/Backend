from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionManager

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(unique=True)  # unique=True 추가

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # 저장 전에 필드값 로깅 -> 이게 왜 로그인할 때마다 뜨지??
        print(f"Saving user with email: {self.email}, phone: {self.phone}, profile_image: {self.profile_image}")
        super().save(*args, **kwargs)
    