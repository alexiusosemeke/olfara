from datetime import timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        VENDOR = "vendor", "Vendor"

    username = None  # removes the username field entirely
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, region="NG", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('email'), name='unique_user_email_ci'),
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']  # noqa: RUF012
    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username}'s account."

    @property
    def getUserName(self):
        return f"{self.first_name} {self.last_name}"