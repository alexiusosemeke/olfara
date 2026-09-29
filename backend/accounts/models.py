from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        VENDOR = "vendor", "Vendor"

    phone = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def __str__(self) -> str:
        return f"{self.username}'s account."


# Create your models here.
