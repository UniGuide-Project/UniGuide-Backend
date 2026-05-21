from django.db import models
from django.conf import settings


class Subject(models.Model):
    """Fan modeli (majburiy yoki tanlanadigan)."""

    class SubjectType(models.TextChoices):
        MANDATORY = 'mandatory', 'Majburiy'
        ELECTIVE = 'elective', 'Tanlanadigan'

    name = models.CharField(max_length=255, verbose_name="Fan nomi")
    subject_type = models.CharField(
        max_length=50,
        choices=SubjectType.choices,
        default=SubjectType.MANDATORY,
        verbose_name="Fan turi",
    )
    img = models.ImageField(upload_to='subjects/', blank=True, null=True, verbose_name="Rasm")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Test narxi (so'm)")

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['subject_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_subject_type_display()}) - {self.price} so'm"


class Question(models.Model):
    """Savol modeli."""

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Fan",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Savol matni")
    img = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Savol rasmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ['-created_at']

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.text and not self.img:
            raise ValidationError("Savol matni yoki rasmidan kamida bittasi kiritilishi shart!")

    def __str__(self):
        if self.text:
            return f"{self.text[:80]}..."
        return f"Savol #{self.id} (Faqat rasm)"


class Choice(models.Model):
    """Variant modeli."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Savol",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Variant matni")
    img = models.ImageField(upload_to='choices/', blank=True, null=True, verbose_name="Variant rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variantlar"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.text and not self.img:
            raise ValidationError("Variant matni yoki rasmidan kamida bittasi kiritilishi shart!")

    def __str__(self):
        mark = "✓" if self.is_correct else "✗"
        if self.text:
            return f"[{mark}] {self.text[:60]}"
        return f"[{mark}] Variant #{self.id} (Faqat rasm)"


class QuizAttempt(models.Model):
    """Foydalanuvchining test yechish urinishi (statistika)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name="Foydalanuvchi",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name="Fan",
    )
    total_questions = models.PositiveIntegerField(verbose_name="Jami savollar")
    correct_answers = models.PositiveIntegerField(verbose_name="To'g'ri javoblar")
    score_percent = models.FloatField(verbose_name="Natija (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yechilgan vaqt")

    class Meta:
        verbose_name = "Test urinishi"
        verbose_name_plural = "Test urinishlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.subject.name} - {self.score_percent}%"


class SystemSetting(models.Model):
    """Tizim sozlamalari (masalan, test narxi)."""

    dtm_test_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=5000.00,
        verbose_name="DTM Test yechish narxi (so'm)",
    )

    class Meta:
        verbose_name = "Tizim sozlamasi"
        verbose_name_plural = "Tizim sozlamalari"

    def __str__(self):
        return f"DTM Test narxi: {self.dtm_test_price} so'm"


def get_dtm_test_price():
    """Tizimdagi DTM test yechish narxini olish (agar yo'q bo'lsa, default yaratadi)."""
    setting = SystemSetting.objects.first()
    if not setting:
        setting = SystemSetting.objects.create()
    return setting.dtm_test_price
