from django.db import models


class University(models.Model):
    """Universitet modeli."""

    UNIVERSITY_TYPES = [
        ('state', 'Davlat'),
        ('private', 'Xususiy'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    img = models.ImageField(upload_to='universities/', blank=True, null=True, verbose_name="Rasm")
    rating = models.BigIntegerField(default=0, verbose_name="Reyting")
    website = models.URLField(max_length=500, blank=True, null=True, verbose_name="Veb-sayt")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lokatsiya")
    university_type = models.CharField(
        max_length=20,
        choices=UNIVERSITY_TYPES,
        default='state',
        verbose_name="Turi"
    )

    class Meta:
        verbose_name = "Universitet"
        verbose_name_plural = "Universitetlar"
        ordering = ['-rating']

    def __str__(self):
        return self.name


class Faculty(models.Model):
    """Fakultet modeli."""

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='faculties',
        verbose_name="Universitet",
    )
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    min_score = models.BigIntegerField(default=0, verbose_name="Minimal ball")
    grant_score = models.BigIntegerField(default=0, verbose_name="Grant ball")

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} — {self.university.name}"
