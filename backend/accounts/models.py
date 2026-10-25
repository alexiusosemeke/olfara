from datetime import timedelta

from core.tokens import generate_token
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
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
    email = models.CharField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa: RUF012
    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username}'s account."

    @property
    def getUserName(self):
        return f"{self.first_name} {self.last_name}"


class AccountVerificationToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verification_token"
    )
    token = models.CharField(max_length=64, default=generate_token, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(hours=2)
        return not self.is_used and timezone.now() < expiration_time

    def __str__(self) -> str:
        return f"{self.user.first_name}'s token"
