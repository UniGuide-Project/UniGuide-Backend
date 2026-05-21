from django.contrib import admin
from .models import CertificateSubject, CertificateQuestion, CertificateChoice, CertificateAttempt


class CertChoiceInline(admin.TabularInline):
    model = CertificateChoice
    extra = 4
    fields = ['text', 'img', 'is_correct']


@admin.register(CertificateSubject)
class CertSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'questions_count']
    search_fields = ['name']

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = "Savollar soni"


@admin.register(CertificateQuestion)
class CertQuestionAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'subject', 'choices_count', 'created_at']
    list_filter = ['subject']
    search_fields = ['text']
    inlines = [CertChoiceInline]

    def short_text(self, obj):
        if obj.text:
            return obj.text[:80]
        return f"Savol #{obj.id} (Faqat rasm)"
    short_text.short_description = "Savol"

    def choices_count(self, obj):
        return obj.choices.count()
    choices_count.short_description = "Variantlar"


@admin.register(CertificateAttempt)
class CertAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'total_questions', 'correct_answers', 'score', 'score_percent', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['user__email', 'subject__name']
    readonly_fields = ['user', 'subject', 'total_questions', 'correct_answers', 'score', 'score_percent', 'created_at']

    def has_add_permission(self, request):
        return False
