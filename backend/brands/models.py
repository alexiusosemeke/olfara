from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

# Create your models here.


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
    )
    country = models.CharField(
        max_length=100,
        blank=True,
    )
    logo = CloudinaryField(
        "image",
        folder="brands/",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class ScentFamily(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Note(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Perfume(models.Model):
    class Concentration(models.TextChoices):
        EDT = ("edt", "Eau De Toilette")
        EDP = ("edp", "Eau De Parfum")
        EXTRAIT = ("extrait", "Extrait De Parfum")

    class Gender(models.TextChoices):
        MEN = ("men", "Men")
        WOMEN = ("women", "Women")
        UNISEX = ("unisex", "Unisex")

    name = models.CharField(
        max_length=150,
        blank=False,
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="perfumes")
    normalized_name = models.CharField(max_length=150, blank=True)
    concentration = models.CharField(
        max_length=50, choices=Concentration.choices, default=Concentration.EDP
    )
    description = models.TextField()
    scent_family = models.ForeignKey(
        ScentFamily, on_delete=models.PROTECT, related_name="perfumes"
    )
    notes = models.ManyToManyField(Note, through="PerfumeNote", related_name="perfumes")
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=False)
    # primary_image = models.ImageField(upload_to="perfumes/main/", blank=True, null=True)
    primary_image = CloudinaryField(
        "image", folder="perfumes/main/", blank=True, null=True
    )
    release_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)],
    )

    def __str__(self) -> str:
        return f"{self.name} by {self.brand.name}"


class PerfumeImage(models.Model):
    perfume = models.ForeignKey(
        Perfume, on_delete=models.CASCADE, related_name="gallery_images"
    )
    # image = models.ImageField(upload_to="perfumes/gallery/")
    image = CloudinaryField("image", folder="perfumes/gallery/")
    caption = models.CharField(
        max_length=100, blank=True, help_text="e.g., Packaging Box"
    )

    def __str__(self) -> str:
        return f"Image for {self.perfume.name}"


class PerfumeNote(models.Model):
    class NoteType(models.TextChoices):
        TOP = "top", "Top (Opening)"
        MIDDLE = "middle", "Middle (Heart)"
        BASE = "base", "Base (Dry-down)"

    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=10, choices=NoteType.choices)

    class Meta:
        # unique_together = ("perfume", "note", "note_type")
        models.UniqueConstraint(
            fields=["perfume", "note", "note_type"], name="unique_perfume_note"
        )

    def __str__(self):
        return (
            f"{self.perfume.name} - {self.note.name} ({self.get_note_type_display()})"
        )
