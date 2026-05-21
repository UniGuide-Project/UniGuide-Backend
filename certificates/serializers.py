from rest_framework import serializers
from .models import CertificateSubject, CertificateQuestion, CertificateChoice, CertificateAttempt


# ─── Choice Serializers ───────────────────────────────────────────────────────

class CertChoiceSerializer(serializers.ModelSerializer):
    """Variant yaratish/yangilash uchun serializer."""

    class Meta:
        model = CertificateChoice
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


class CertChoiceDetailSerializer(serializers.ModelSerializer):
    """Variant ko'rish uchun (to'g'ri javob yashirin)."""

    class Meta:
        model = CertificateChoice
        fields = ['id', 'text', 'img']
        read_only_fields = ['id']


class CertChoiceWithAnswerSerializer(serializers.ModelSerializer):
    """Variant ko'rish uchun (to'g'ri javob ko'rsatiladi — admin/natija uchun)."""

    class Meta:
        model = CertificateChoice
        fields = ['id', 'text', 'img', 'is_correct']
        read_only_fields = ['id']


# ─── Question Serializers ─────────────────────────────────────────────────────

class CertQuestionListSerializer(serializers.ModelSerializer):
    """Savollar ro'yxati uchun serializer."""

    subject_name = serializers.CharField(source='subject.name', read_only=True)
    choices_count = serializers.IntegerField(source='choices.count', read_only=True)

    class Meta:
        model = CertificateQuestion
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class CertQuestionDetailSerializer(serializers.ModelSerializer):
    """Savol tafsilotlari — variantlari bilan (to'g'ri javob yashirin)."""

    choices = CertChoiceDetailSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = CertificateQuestion
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices', 'created_at']
        read_only_fields = ['id', 'created_at']


class CertQuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Savol tafsilotlari — to'g'ri javob ko'rinadi (admin uchun)."""

    choices = CertChoiceWithAnswerSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = CertificateQuestion
        fields = ['id', 'subject', 'subject_name', 'text', 'img', 'choices', 'created_at']
        read_only_fields = ['id', 'created_at']


class CertQuestionCreateSerializer(serializers.ModelSerializer):
    """Savol yaratish/yangilash uchun serializer."""

    class Meta:
        model = CertificateQuestion
        fields = ['id', 'subject', 'text', 'img']
        read_only_fields = ['id']

    def validate(self, attrs):
        text = attrs.get('text')
        img = attrs.get('img')
        if self.instance:
            text = text if 'text' in attrs else self.instance.text
            img = img if 'img' in attrs else self.instance.img
        if not text and not img:
            raise serializers.ValidationError("Savol matni yoki rasmidan kamida bittasi kiritilishi shart!")
        return attrs


# ─── Subject Serializers ──────────────────────────────────────────────────────

class CertSubjectListSerializer(serializers.ModelSerializer):
    """Fanlar ro'yxati uchun serializer."""

    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = CertificateSubject
        fields = ['id', 'name', 'img', 'questions_count']
        read_only_fields = ['id']


class CertSubjectDetailSerializer(serializers.ModelSerializer):
    """Fan tafsilotlari."""

    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = CertificateSubject
        fields = ['id', 'name', 'img', 'questions_count']
        read_only_fields = ['id']


class CertSubjectCreateSerializer(serializers.ModelSerializer):
    """Fan yaratish/yangilash uchun serializer."""

    class Meta:
        model = CertificateSubject
        fields = ['id', 'name', 'img']
        read_only_fields = ['id']


# ─── Attempt Serializer ──────────────────────────────────────────────────────

class CertAttemptSerializer(serializers.ModelSerializer):
    """Sertifikat test urinishi (statistika) uchun serializer."""

    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = CertificateAttempt
        fields = ['id', 'subject', 'subject_name', 'total_questions', 'correct_answers', 'score', 'score_percent', 'created_at']
        read_only_fields = ['id', 'created_at']
