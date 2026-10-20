from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=100)
    country = models.CharField(blank=True)
    logo = models.ImageField(upload_to="brands/", blank=True)

    def __str__(self) -> str:
        return self.name
