from rest_framework import serializers
from .models import Subject, Question, Choice, QuizAttempt


# ─── Choice Serializers ───────────────────────────────────────────────────────

class ChoiceSerializer(serializers.ModelSerializer):
    """Variant yaratish/yangilash uchun serializer."""

    class Meta:
        model = Choice
        fields = ['id', 'question', 'text', 'img', 'is_correct']
        read_only_fields = ['id']

    def validate(self, attrs):
        text = attrs.get('text')
        img = attrs.get('img')

        if self.instance:
            text = text if 'text' in attrs else self.instance.text
            img = img if 'img' in attrs else self.instance.img

        if not text and not img:
            raise serializers.ValidationError("Variant matni yoki rasmidan kamida bittasi kiritilishi shart!")
        return attrs


class ChoiceDetailSerializer(serializers.ModelSerializer):
    """Variant ko'rish uchun (to'g'ri javob ko'rsatilmaydi)."""

    class Meta:
        model = Choice
        fields = ['id', 'text', 'img']
        read_only_fields = ['id']


class ChoiceWithAnswerSerializer(serializers.ModelSerializer):
    """Variant ko'rish uchun (to'g'ri javob ko'rsatiladi — admin/natija uchun)."""

    class Meta:
        model = Choice
        fields = ['id', 'text', 'img', 'is_correct']
        read_only_fields = ['id']


# ─── Question Serializers ─────────────────────────────────────────────────────

class QuestionListSerializer(serializers.ModelSerializer):
    """Savollar ro'yxati uchun serializer."""

    subject_name = serializers.CharField(source='subject.name', read_only=True)
    choices_count = serializers.IntegerField(source='choices.count', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Savol tafsilotlari — variantlari bilan (to'g'ri javob yashirin)."""

    choices = ChoiceDetailSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Savol tafsilotlari — variantlari bilan (to'g'ri javob ko'rinadi — admin uchun)."""

    choices = ChoiceWithAnswerSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Savol yaratish/yangilash uchun serializer."""

    class Meta:
        model = Question
        fields = ['id', 'subject', 'text', 'img']
        read_only_fields = ['id']

    def validate(self, attrs):
        text = attrs.get('text')
        img = attrs.get('img')

        # Agar yangilanish (update) bo'layotgan bo'lsa va yangi ma'lumotlarda yuborilmagan bo'lsa,
        # bazadagi joriy qiymatlarni hisobga olamiz.
        if self.instance:
            text = text if 'text' in attrs else self.instance.text
            img = img if 'img' in attrs else self.instance.img

        if not text and not img:
            raise serializers.ValidationError("Savol matni yoki rasmidan kamida bittasi kiritilishi shart!")
        return attrs


# ─── Subject Serializers ──────────────────────────────────────────────────────

class SubjectListSerializer(serializers.ModelSerializer):
    """Fanlar ro'yxati uchun serializer."""

    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    subject_type_display = serializers.CharField(source='get_subject_type_display', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_type', 'subject_type_display', 'img', 'questions_count']
        read_only_fields = ['id']


class SubjectDetailSerializer(serializers.ModelSerializer):
    """Fan tafsilotlari — savollar soni bilan."""

    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    subject_type_display = serializers.CharField(source='get_subject_type_display', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_type', 'subject_type_display', 'img', 'questions_count']
        read_only_fields = ['id']


class SubjectCreateSerializer(serializers.ModelSerializer):
    """Fan yaratish/yangilash uchun serializer."""

    class Meta:
        model = Subject
        fields = ['id', 'name', 'subject_type', 'img']
        read_only_fields = ['id']


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Test urinishi (statistika) uchun serializer."""

    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_type_display = serializers.CharField(source='subject.get_subject_type_display', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'subject', 'subject_name', 'subject_type_display', 'total_questions', 'correct_answers', 'score_percent', 'created_at']
        read_only_fields = ['id', 'created_at']
