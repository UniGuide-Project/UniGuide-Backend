from django.contrib import admin
from .models import Subject, Question, Choice, QuizAttempt, SystemSetting


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ['text', 'img', 'is_correct']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_type', 'questions_count']
    list_filter = ['subject_type']
    search_fields = ['name']

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = "Savollar soni"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'subject', 'choices_count', 'created_at']
    list_filter = ['subject']
    search_fields = ['text']
    inlines = [ChoiceInline]

    def short_text(self, obj):
        return obj.text[:80]
    short_text.short_description = "Savol"

    def choices_count(self, obj):
        return obj.choices.count()
    choices_count.short_description = "Variantlar"


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'total_questions', 'correct_answers', 'score_percent', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['user__email', 'subject__name']
    readonly_fields = ['user', 'subject', 'total_questions', 'correct_answers', 'score_percent', 'created_at']

    # Adminlar yangi test natijasi qo'sha olishmasin (faqat ko'rishsin)
    def has_add_permission(self, request):
        return False


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['dtm_test_price']

    def has_add_permission(self, request):
        # Agar tizimda allaqachon sozlama yaratilgan bo'lsa, ikkinchisini qo'shishni cheklaymiz
        if SystemSetting.objects.exists():
            return False
        return True
