from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Khách hàng'),
        ('admin', 'Quản trị viên'),
        ('maintenance_staff', 'Nhân viên bảo trì'),
    ]
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_maintenance_staff(self):
        return self.role == 'maintenance_staff'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    company = models.CharField(max_length=200, blank=True)
    tax_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
