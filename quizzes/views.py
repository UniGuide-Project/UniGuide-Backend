from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction
from .models import Subject, Question, Choice, QuizAttempt, get_dtm_test_price
from .serializers import (
    SubjectListSerializer,
    SubjectDetailSerializer,
    SubjectCreateSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    QuestionWithAnswerSerializer,
    QuestionCreateSerializer,
    ChoiceSerializer,
    ChoiceWithAnswerSerializer,
    QuizAttemptSerializer,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  FANLAR (Subjects)
# ═══════════════════════════════════════════════════════════════════════════════

class SubjectListView(generics.ListAPIView):
    """Barcha fanlar ro'yxati. Filtrlash: ?type=mandatory yoki ?type=elective"""
    serializer_class = SubjectListSerializer
    permission_classes = [AllowAny]

    type_param = openapi.Parameter(
        'type', openapi.IN_QUERY,
        description="Fan turi bo'yicha filtrlash: mandatory yoki elective",
        type=openapi.TYPE_STRING,
        enum=['mandatory', 'elective'],
        required=False,
    )

    def get_queryset(self):
        queryset = Subject.objects.all()
        subject_type = self.request.query_params.get('type')
        if subject_type in ['mandatory', 'elective']:
            queryset = queryset.filter(subject_type=subject_type)
        return queryset

    @swagger_auto_schema(
        operation_summary="Fanlar ro'yxati",
        operation_description="Barcha fanlar. Filtrlash: ?type=mandatory yoki ?type=elective",
        manual_parameters=[type_param],
        responses={200: SubjectListSerializer(many=True)},
        tags=['DTM — Fanlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubjectDetailView(generics.RetrieveAPIView):
    """Bitta fan tafsilotlari."""
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Fan tafsilotlari",
        responses={200: SubjectDetailSerializer},
        tags=['DTM — Fanlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubjectCreateView(generics.CreateAPIView):
    """Yangi fan yaratish (Admin)."""
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fan yaratish (Admin)",
        request_body=SubjectCreateSerializer,
        responses={201: SubjectCreateSerializer},
        tags=['DTM — Fanlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubjectUpdateView(generics.UpdateAPIView):
    """Fanni yangilash (Admin)."""
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fanni yangilash (Admin)",
        request_body=SubjectCreateSerializer,
        responses={200: SubjectCreateSerializer},
        tags=['DTM — Fanlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fanni qisman yangilash (Admin)",
        request_body=SubjectCreateSerializer,
        responses={200: SubjectCreateSerializer},
        tags=['DTM — Fanlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class SubjectDeleteView(generics.DestroyAPIView):
    """Fanni o'chirish (Admin)."""
    queryset = Subject.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fanni o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['DTM — Fanlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  SAVOLLAR (Questions)
# ═══════════════════════════════════════════════════════════════════════════════

class QuestionListView(generics.ListAPIView):
    """
    Savollar ro'yxati.
    Filtrlash: ?subject=<id> — fanga tegishli savollar.
    """
    serializer_class = QuestionListSerializer
    permission_classes = [AllowAny]

    subject_param = openapi.Parameter(
        'subject', openapi.IN_QUERY,
        description="Fan ID bo'yicha filtrlash",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    def get_queryset(self):
        queryset = Question.objects.select_related('subject').all()
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Savollar ro'yxati",
        operation_description="Barcha savollar yoki fan bo'yicha filtrlangan.",
        manual_parameters=[subject_param],
        responses={200: QuestionListSerializer(many=True)},
        tags=['DTM — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveAPIView):
    """Savol tafsilotlari — variantlari bilan (to'g'ri javob yashirin)."""
    queryset = Question.objects.prefetch_related('choices').select_related('subject').all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Savol tafsilotlari (variantlar bilan)",
        operation_description="To'g'ri javob ko'rsatilmaydi — foydalanuvchi uchun.",
        responses={200: QuestionDetailSerializer},
        tags=['DTM — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuestionDetailAdminView(generics.RetrieveAPIView):
    """Savol tafsilotlari — to'g'ri javoblar ko'rinadi (Admin)."""
    queryset = Question.objects.prefetch_related('choices').select_related('subject').all()
    serializer_class = QuestionWithAnswerSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Savol tafsilotlari — javoblar bilan (Admin)",
        operation_description="To'g'ri javoblar ko'rsatiladi — faqat admin uchun.",
        responses={200: QuestionWithAnswerSerializer},
        tags=['DTM — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuestionCreateView(generics.CreateAPIView):
    """Yangi savol yaratish (Admin)."""
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Savol yaratish (Admin)",
        request_body=QuestionCreateSerializer,
        responses={201: QuestionCreateSerializer},
        tags=['DTM — Savollar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuestionUpdateView(generics.UpdateAPIView):
    """Savolni yangilash (Admin)."""
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Savolni yangilash (Admin)",
        request_body=QuestionCreateSerializer,
        responses={200: QuestionCreateSerializer},
        tags=['DTM — Savollar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Savolni qisman yangilash (Admin)",
        request_body=QuestionCreateSerializer,
        responses={200: QuestionCreateSerializer},
        tags=['DTM — Savollar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class QuestionDeleteView(generics.DestroyAPIView):
    """Savolni o'chirish (Admin)."""
    queryset = Question.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Savolni o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['DTM — Savollar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  VARIANTLAR (Choices)
# ═══════════════════════════════════════════════════════════════════════════════

class ChoiceListView(generics.ListAPIView):
    """
    Variantlar ro'yxati (Admin).
    Filtrlash: ?question=<id>
    """
    serializer_class = ChoiceWithAnswerSerializer
    permission_classes = [IsAdminUser]

    question_param = openapi.Parameter(
        'question', openapi.IN_QUERY,
        description="Savol ID bo'yicha filtrlash",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    def get_queryset(self):
        queryset = Choice.objects.all()
        question_id = self.request.query_params.get('question')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Variantlar ro'yxati (Admin)",
        manual_parameters=[question_param],
        responses={200: ChoiceWithAnswerSerializer(many=True)},
        tags=['DTM — Variantlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChoiceCreateView(generics.CreateAPIView):
    """Yangi variant yaratish (Admin)."""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Variant yaratish (Admin)",
        request_body=ChoiceSerializer,
        responses={201: ChoiceSerializer},
        tags=['DTM — Variantlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ChoiceUpdateView(generics.UpdateAPIView):
    """Variantni yangilash (Admin)."""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Variantni yangilash (Admin)",
        request_body=ChoiceSerializer,
        responses={200: ChoiceSerializer},
        tags=['DTM — Variantlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Variantni qisman yangilash (Admin)",
        request_body=ChoiceSerializer,
        responses={200: ChoiceSerializer},
        tags=['DTM — Variantlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChoiceDeleteView(generics.DestroyAPIView):
    """Variantni o'chirish (Admin)."""
    queryset = Choice.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Variantni o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['DTM — Variantlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST TEKSHIRISH
# ═══════════════════════════════════════════════════════════════════════════════

class CheckAnswersView(APIView):
    """
    Foydalanuvchi javoblarini tekshirish.

    Request body: {"answers": [{"question_id": 1, "choice_id": 3}, ...]}
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Javoblarni tekshirish",
        operation_description=(
            "Foydalanuvchi tanlagan javoblarni tekshirish.\n\n"
            "Format: `{\"answers\": [{\"question_id\": 1, \"choice_id\": 3}, ...]}`"
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['answers'],
            properties={
                'answers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'choice_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Natija",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'correct': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'wrong': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'score_percent': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    }
                ),
            ),
        },
        tags=['DTM — Test'],
    )
    def post(self, request):
        answers = request.data.get('answers', [])
        if not answers:
            return Response(
                {'error': "Javoblar ro'yxati bo'sh!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = []
        correct_count = 0

        for answer in answers:
            question_id = answer.get('question_id')
            choice_id = answer.get('choice_id')

            try:
                choice = Choice.objects.select_related('question').get(
                    id=choice_id,
                    question_id=question_id,
                )
                is_correct = choice.is_correct
                correct_choice = Choice.objects.filter(
                    question_id=question_id,
                    is_correct=True,
                ).first()

                if is_correct:
                    correct_count += 1

                results.append({
                    'question_id': question_id,
                    'your_choice_id': choice_id,
                    'is_correct': is_correct,
                    'correct_choice_id': correct_choice.id if correct_choice else None,
                })
            except Choice.DoesNotExist:
                results.append({
                    'question_id': question_id,
                    'your_choice_id': choice_id,
                    'is_correct': False,
                    'error': "Noto'g'ri savol yoki variant ID",
                })

        total = len(answers)
        score_percent = round((correct_count / total) * 100, 1) if total > 0 else 0

        # Avtomatik ravishda foydalanuvchi statistikasini saqlash
        if total > 0 and request.user.is_authenticated:
            first_q_id = answers[0].get('question_id')
            try:
                first_q = Question.objects.select_related('subject').get(id=first_q_id)
                QuizAttempt.objects.create(
                    user=request.user,
                    subject=first_q.subject,
                    total_questions=total,
                    correct_answers=correct_count,
                    score_percent=score_percent
                )
            except Question.DoesNotExist:
                pass

        return Response({
            'total': total,
            'correct': correct_count,
            'wrong': total - correct_count,
            'score_percent': score_percent,
            'details': results,
        }, status=status.HTTP_200_OK)


class StartTestView(APIView):
    """
    Test boshlanishi — random tartibdagi savollar.
    Query: ?subject=1&limit=10
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Testni boshlash (Tasodifiy savollar)",
        operation_description=(
            "Berilgan fandan tasodifiy tartibdagi savollarni qaytaradi.\n"
            "Query: `?subject=<subject_id>&limit=<savollar_soni>`"
        ),
        manual_parameters=[
            openapi.Parameter('subject', openapi.IN_QUERY, description="Fan ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Savollar soni (default: 10)", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={200: QuestionDetailSerializer(many=True)},
        tags=['DTM — Test'],
    )
    @transaction.atomic
    def get(self, request):
        subject_id = request.query_params.get('subject')
        if not subject_id:
            return Response(
                {'error': "subject (fan ID) ko'rsatilishi shart!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            limit = 10

        # Tasodifiy tartibdagi savollar
        questions = Question.objects.filter(subject_id=subject_id).order_by('?')[:limit]
        serializer = QuestionDetailSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserStatisticsView(generics.ListAPIView):
    """Foydalanuvchining test yechish urinishlari statistikasi (tarixi)."""
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('subject')

    @swagger_auto_schema(
        operation_summary="Foydalanuvchi test statistikasi",
        operation_description="Joriy foydalanuvchining barcha yechgan testlari natijalari.",
        responses={200: QuizAttemptSerializer(many=True)},
        tags=['DTM — Test'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
