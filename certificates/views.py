from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CertificateSubject, CertificateQuestion, CertificateChoice, CertificateAttempt
from .serializers import (
    CertSubjectListSerializer, CertSubjectDetailSerializer, CertSubjectCreateSerializer,
    CertQuestionListSerializer, CertQuestionDetailSerializer, CertQuestionWithAnswerSerializer,
    CertQuestionCreateSerializer,
    CertChoiceSerializer, CertChoiceWithAnswerSerializer,
    CertAttemptSerializer,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  FANLAR (Certificate Subjects)
# ═══════════════════════════════════════════════════════════════════════════════

class CertSubjectListView(generics.ListAPIView):
    """Barcha sertifikat fanlari ro'yxati."""
    serializer_class = CertSubjectListSerializer
    permission_classes = [AllowAny]
    queryset = CertificateSubject.objects.all()

    @swagger_auto_schema(
        operation_summary="Sertifikat fanlari ro'yxati",
        operation_description="Milliy sertifikat uchun barcha fanlar (tillar yo'q).",
        responses={200: CertSubjectListSerializer(many=True)},
        tags=['Sertifikat — Fanlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertSubjectDetailView(generics.RetrieveAPIView):
    """Bitta sertifikat fan tafsilotlari."""
    queryset = CertificateSubject.objects.all()
    serializer_class = CertSubjectDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Sertifikat fani tafsilotlari",
        responses={200: CertSubjectDetailSerializer},
        tags=['Sertifikat — Fanlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertSubjectCreateView(generics.CreateAPIView):
    """Yangi sertifikat fani yaratish (Admin)."""
    queryset = CertificateSubject.objects.all()
    serializer_class = CertSubjectCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat fani yaratish (Admin)",
        request_body=CertSubjectCreateSerializer,
        responses={201: CertSubjectCreateSerializer},
        tags=['Sertifikat — Fanlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CertSubjectUpdateView(generics.UpdateAPIView):
    """Sertifikat fanini yangilash (Admin)."""
    queryset = CertificateSubject.objects.all()
    serializer_class = CertSubjectCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat fanini yangilash (Admin)",
        request_body=CertSubjectCreateSerializer,
        responses={200: CertSubjectCreateSerializer},
        tags=['Sertifikat — Fanlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Sertifikat fanini qisman yangilash (Admin)",
        request_body=CertSubjectCreateSerializer,
        responses={200: CertSubjectCreateSerializer},
        tags=['Sertifikat — Fanlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CertSubjectDeleteView(generics.DestroyAPIView):
    """Sertifikat fanini o'chirish (Admin)."""
    queryset = CertificateSubject.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat fanini o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Sertifikat — Fanlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  SAVOLLAR (Certificate Questions)
# ═══════════════════════════════════════════════════════════════════════════════

class CertQuestionListView(generics.ListAPIView):
    """Sertifikat savollari ro'yxati. Filtrlash: ?subject=<id>"""
    serializer_class = CertQuestionListSerializer
    permission_classes = [AllowAny]

    subject_param = openapi.Parameter(
        'subject', openapi.IN_QUERY,
        description="Fan ID bo'yicha filtrlash",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    def get_queryset(self):
        queryset = CertificateQuestion.objects.select_related('subject').all()
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Sertifikat savollari ro'yxati",
        operation_description="Barcha savollar yoki fan bo'yicha filtrlangan.",
        manual_parameters=[subject_param],
        responses={200: CertQuestionListSerializer(many=True)},
        tags=['Sertifikat — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertQuestionDetailView(generics.RetrieveAPIView):
    """Sertifikat savol tafsilotlari — variantlari bilan (to'g'ri javob yashirin)."""
    queryset = CertificateQuestion.objects.prefetch_related('choices').select_related('subject').all()
    serializer_class = CertQuestionDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Sertifikat savol tafsilotlari",
        responses={200: CertQuestionDetailSerializer},
        tags=['Sertifikat — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertQuestionDetailAdminView(generics.RetrieveAPIView):
    """Sertifikat savol tafsilotlari — to'g'ri javoblar ko'rinadi (Admin)."""
    queryset = CertificateQuestion.objects.prefetch_related('choices').select_related('subject').all()
    serializer_class = CertQuestionWithAnswerSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat savol tafsilotlari — javoblar bilan (Admin)",
        responses={200: CertQuestionWithAnswerSerializer},
        tags=['Sertifikat — Savollar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertQuestionCreateView(generics.CreateAPIView):
    """Yangi sertifikat savoli yaratish (Admin)."""
    queryset = CertificateQuestion.objects.all()
    serializer_class = CertQuestionCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat savoli yaratish (Admin)",
        request_body=CertQuestionCreateSerializer,
        responses={201: CertQuestionCreateSerializer},
        tags=['Sertifikat — Savollar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CertQuestionUpdateView(generics.UpdateAPIView):
    """Sertifikat savolini yangilash (Admin)."""
    queryset = CertificateQuestion.objects.all()
    serializer_class = CertQuestionCreateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat savolini yangilash (Admin)",
        request_body=CertQuestionCreateSerializer,
        responses={200: CertQuestionCreateSerializer},
        tags=['Sertifikat — Savollar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Sertifikat savolini qisman yangilash (Admin)",
        request_body=CertQuestionCreateSerializer,
        responses={200: CertQuestionCreateSerializer},
        tags=['Sertifikat — Savollar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CertQuestionDeleteView(generics.DestroyAPIView):
    """Sertifikat savolini o'chirish (Admin)."""
    queryset = CertificateQuestion.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat savolini o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Sertifikat — Savollar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  VARIANTLAR (Certificate Choices)
# ═══════════════════════════════════════════════════════════════════════════════

class CertChoiceListView(generics.ListAPIView):
    """Sertifikat variantlari ro'yxati (Admin). Filtrlash: ?question=<id>"""
    serializer_class = CertChoiceWithAnswerSerializer
    permission_classes = [IsAdminUser]

    question_param = openapi.Parameter(
        'question', openapi.IN_QUERY,
        description="Savol ID bo'yicha filtrlash",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    def get_queryset(self):
        queryset = CertificateChoice.objects.all()
        question_id = self.request.query_params.get('question')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Sertifikat variantlari ro'yxati (Admin)",
        manual_parameters=[question_param],
        responses={200: CertChoiceWithAnswerSerializer(many=True)},
        tags=['Sertifikat — Variantlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CertChoiceCreateView(generics.CreateAPIView):
    """Yangi sertifikat varianti yaratish (Admin)."""
    queryset = CertificateChoice.objects.all()
    serializer_class = CertChoiceSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat varianti yaratish (Admin)",
        request_body=CertChoiceSerializer,
        responses={201: CertChoiceSerializer},
        tags=['Sertifikat — Variantlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CertChoiceUpdateView(generics.UpdateAPIView):
    """Sertifikat variantini yangilash (Admin)."""
    queryset = CertificateChoice.objects.all()
    serializer_class = CertChoiceSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat variantini yangilash (Admin)",
        request_body=CertChoiceSerializer,
        responses={200: CertChoiceSerializer},
        tags=['Sertifikat — Variantlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Sertifikat variantini qisman yangilash (Admin)",
        request_body=CertChoiceSerializer,
        responses={200: CertChoiceSerializer},
        tags=['Sertifikat — Variantlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CertChoiceDeleteView(generics.DestroyAPIView):
    """Sertifikat variantini o'chirish (Admin)."""
    queryset = CertificateChoice.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Sertifikat variantini o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Sertifikat — Variantlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST BOSHLASH VA TEKSHIRISH
# ═══════════════════════════════════════════════════════════════════════════════

class CertStartTestView(APIView):
    """
    Sertifikat testini boshlash — tasodifiy savollar.
    Query: ?subject=<id>&limit=<son>
    Demo versiya: bepul.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Sertifikat testini boshlash",
        operation_description=(
            "Berilgan fandan tasodifiy tartibdagi savollarni qaytaradi.\n"
            "Demo versiya: bepul.\n\n"
            "Query: `?subject=<subject_id>&limit=<savollar_soni>`"
        ),
        manual_parameters=[
            openapi.Parameter('subject', openapi.IN_QUERY, description="Fan ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Savollar soni (default: 30)", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={200: CertQuestionDetailSerializer(many=True)},
        tags=['Sertifikat — Test'],
    )
    def get(self, request):
        subject_id = request.query_params.get('subject')
        if not subject_id:
            return Response(
                {'error': "subject (fan ID) ko'rsatilishi shart!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not CertificateSubject.objects.filter(id=subject_id).exists():
            return Response(
                {'error': "Bunday fan topilmadi!"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            limit = int(request.query_params.get('limit', 30))
        except ValueError:
            limit = 30

        questions = CertificateQuestion.objects.filter(subject_id=subject_id).order_by('?')[:limit]
        serializer = CertQuestionDetailSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CertCheckAnswersView(APIView):
    """
    Sertifikat test javoblarini tekshirish.
    Baholash: 1 to'g'ri javob = 1 ball (manfiy ball yo'q).

    Request body: {"answers": [{"question_id": 1, "choice_id": 3}, ...]}
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Sertifikat javoblarini tekshirish",
        operation_description=(
            "Foydalanuvchi tanlagan javoblarni tekshirish.\n\n"
            "**Baholash mezoni:** 1 to'g'ri javob = 1 ball (manfiy ball yo'q).\n\n"
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
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description="Jami savollar"),
                        'correct': openapi.Schema(type=openapi.TYPE_INTEGER, description="To'g'ri javoblar"),
                        'wrong': openapi.Schema(type=openapi.TYPE_INTEGER, description="Noto'g'ri javoblar"),
                        'score': openapi.Schema(type=openapi.TYPE_INTEGER, description="Ball (1 to'g'ri = 1 ball)"),
                        'score_percent': openapi.Schema(type=openapi.TYPE_NUMBER, description="Natija (%)"),
                        'details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    }
                ),
            ),
        },
        tags=['Sertifikat — Test'],
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
                choice = CertificateChoice.objects.select_related('question').get(
                    id=choice_id,
                    question_id=question_id,
                )
                is_correct = choice.is_correct
                correct_choice = CertificateChoice.objects.filter(
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
            except CertificateChoice.DoesNotExist:
                results.append({
                    'question_id': question_id,
                    'your_choice_id': choice_id,
                    'is_correct': False,
                    'error': "Noto'g'ri savol yoki variant ID",
                })

        total = len(answers)
        # Baholash mezoni: 1 to'g'ri = 1 ball
        score = correct_count
        score_percent = round((correct_count / total) * 100, 1) if total > 0 else 0

        # Statistikani saqlash
        if total > 0 and request.user.is_authenticated:
            first_q_id = answers[0].get('question_id')
            try:
                first_q = CertificateQuestion.objects.select_related('subject').get(id=first_q_id)
                CertificateAttempt.objects.create(
                    user=request.user,
                    subject=first_q.subject,
                    total_questions=total,
                    correct_answers=correct_count,
                    score=score,
                    score_percent=score_percent,
                )
            except CertificateQuestion.DoesNotExist:
                pass

        return Response({
            'total': total,
            'correct': correct_count,
            'wrong': total - correct_count,
            'score': score,
            'score_percent': score_percent,
            'details': results,
        }, status=status.HTTP_200_OK)


class CertUserStatisticsView(generics.ListAPIView):
    """Foydalanuvchining sertifikat test yechish urinishlari tarixi."""
    serializer_class = CertAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CertificateAttempt.objects.filter(user=self.request.user).select_related('subject')

    @swagger_auto_schema(
        operation_summary="Sertifikat test statistikasi",
        operation_description="Joriy foydalanuvchining barcha sertifikat test natijalari.",
        responses={200: CertAttemptSerializer(many=True)},
        tags=['Sertifikat — Test'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
