from django.db import models
from django.conf import settings


class CertificateSubject(models.Model):
    """Milliy sertifikat fan modeli (tillar yo'q)."""

    name = models.CharField(max_length=255, verbose_name="Fan nomi")
    img = models.ImageField(upload_to='certificate_subjects/', blank=True, null=True, verbose_name="Rasm")

    class Meta:
        verbose_name = "Sertifikat fani"
        verbose_name_plural = "Sertifikat fanlari"
        ordering = ['name']

    def __str__(self):
        return self.name


class CertificateQuestion(models.Model):
    """Sertifikat savol modeli."""

    subject = models.ForeignKey(
        CertificateSubject,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Fan",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Savol matni")
    img = models.ImageField(upload_to='certificate_questions/', blank=True, null=True, verbose_name="Savol rasmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Sertifikat savoli"
        verbose_name_plural = "Sertifikat savollari"
        ordering = ['-created_at']

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.text and not self.img:
            raise ValidationError("Savol matni yoki rasmidan kamida bittasi kiritilishi shart!")

    def __str__(self):
        if self.text:
            return f"{self.text[:80]}..."
        return f"Savol #{self.id} (Faqat rasm)"


class CertificateChoice(models.Model):
    """Sertifikat variant modeli."""

    question = models.ForeignKey(
        CertificateQuestion,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Savol",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Variant matni")
    img = models.ImageField(upload_to='certificate_choices/', blank=True, null=True, verbose_name="Variant rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")

    class Meta:
        verbose_name = "Sertifikat varianti"
        verbose_name_plural = "Sertifikat variantlari"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.text and not self.img:
            raise ValidationError("Variant matni yoki rasmidan kamida bittasi kiritilishi shart!")

    def __str__(self):
        mark = "✓" if self.is_correct else "✗"
        if self.text:
            return f"[{mark}] {self.text[:60]}"
        return f"[{mark}] Variant #{self.id} (Faqat rasm)"


class CertificateAttempt(models.Model):
    """Foydalanuvchining sertifikat test urinishi. Baholash: 1 to'g'ri = 1 ball."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificate_attempts',
        verbose_name="Foydalanuvchi",
    )
    subject = models.ForeignKey(
        CertificateSubject,
        on_delete=models.CASCADE,
        related_name='certificate_attempts',
        verbose_name="Fan",
    )
    total_questions = models.PositiveIntegerField(verbose_name="Jami savollar")
    correct_answers = models.PositiveIntegerField(verbose_name="To'g'ri javoblar")
    score = models.PositiveIntegerField(verbose_name="Ball (1 to'g'ri = 1 ball)")
    score_percent = models.FloatField(verbose_name="Natija (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yechilgan vaqt")

    class Meta:
        verbose_name = "Sertifikat test urinishi"
        verbose_name_plural = "Sertifikat test urinishlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.subject.name} - {self.score}/{self.total_questions} ball"
