from brands.models import Perfume
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class VendorProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_profile",
    )
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    contact_phone = PhoneNumberField(region="NG", blank=True)  # type: ignore
    whatsapp_phone = PhoneNumberField(region="NG")  # type: ignore
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.business_name

    @property
    def whatsapp_link(self) -> str:
        number = self.whatsapp_phone.as_e164.lstrip("+")
        return f"https://wa.me/{number}"


class StockListing(models.Model):
    vendor = models.ForeignKey(
        VendorProfile, on_delete=models.CASCADE, related_name="stock_listings"
    )
    perfume = models.ForeignKey(
        Perfume, on_delete=models.CASCADE, related_name="stock_listings"
    )
    size_ml = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], help_text="Bottle size in milliliters"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    in_stock = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "perfume", "size_ml"],
                name="unique_vendor_perfume_size",
            )
        ]
        indexes = [
            models.Index(fields=["perfume", "in_stock"]),
        ]

    def __str__(self) -> str:
        return f"{self.perfume} ({self.size_ml}ml) - {self.vendor}"
