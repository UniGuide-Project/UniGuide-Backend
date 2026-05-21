from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import University, Faculty
from .serializers import (
    UniversityListSerializer,
    UniversityDetailSerializer,
    FacultySerializer,
    FacultyListSerializer,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  UNIVERSITETLAR
# ═══════════════════════════════════════════════════════════════════════════════

class UniversityListView(generics.ListAPIView):
    """
    Barcha universitetlar ro'yxati.

    Har bir universitetning nomi, tavsifi, rasmi, reytingi
    va fakultetlar soni ko'rsatiladi.
    """
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Universitetlar ro'yxati",
        operation_description="Barcha universitetlarni reyting bo'yicha tartiblangan holda olish.",
        responses={200: UniversityListSerializer(many=True)},
        tags=['Universitetlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UniversityDetailView(generics.RetrieveAPIView):
    """
    Bitta universitet batafsil — fakultetlari bilan.
    """
    queryset = University.objects.prefetch_related('faculties').all()
    serializer_class = UniversityDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Universitet tafsilotlari",
        operation_description="ID orqali bitta universitetning to'liq ma'lumotlari va fakultetlari.",
        responses={200: UniversityDetailSerializer},
        tags=['Universitetlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UniversityCreateView(generics.CreateAPIView):
    """Yangi universitet yaratish (faqat admin)."""
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Universitet yaratish (Admin)",
        operation_description="Yangi universitet qo'shish — faqat admin uchun.",
        request_body=UniversityListSerializer,
        responses={201: UniversityListSerializer},
        tags=['Universitetlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UniversityUpdateView(generics.UpdateAPIView):
    """Universitetni yangilash (faqat admin)."""
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Universitetni yangilash (Admin)",
        request_body=UniversityListSerializer,
        responses={200: UniversityListSerializer},
        tags=['Universitetlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Universitetni qisman yangilash (Admin)",
        request_body=UniversityListSerializer,
        responses={200: UniversityListSerializer},
        tags=['Universitetlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UniversityDeleteView(generics.DestroyAPIView):
    """Universitetni o'chirish (faqat admin)."""
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Universitetni o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Universitetlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  FAKULTETLAR
# ═══════════════════════════════════════════════════════════════════════════════

class FacultyListView(generics.ListAPIView):
    """
    Barcha fakultetlar ro'yxati.

    Ixtiyoriy: ?university=<id> orqali ma'lum universitetning
    fakultetlarini filtrlash mumkin.
    """
    serializer_class = FacultyListSerializer
    permission_classes = [AllowAny]

    university_param = openapi.Parameter(
        'university', openapi.IN_QUERY,
        description="Universitet ID bo'yicha filtrlash",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    def get_queryset(self):
        queryset = Faculty.objects.select_related('university').all()
        university_id = self.request.query_params.get('university')
        if university_id:
            queryset = queryset.filter(university_id=university_id)
        return queryset

    @swagger_auto_schema(
        operation_summary="Fakultetlar ro'yxati",
        operation_description="Barcha fakultetlar yoki universitet bo'yicha filtrlangan ro'yxat.",
        manual_parameters=[university_param],
        responses={200: FacultyListSerializer(many=True)},
        tags=['Fakultetlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FacultyDetailView(generics.RetrieveAPIView):
    """Bitta fakultet tafsilotlari."""
    queryset = Faculty.objects.select_related('university').all()
    serializer_class = FacultyListSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Fakultet tafsilotlari",
        operation_description="ID orqali bitta fakultetning to'liq ma'lumotlari.",
        responses={200: FacultyListSerializer},
        tags=['Fakultetlar'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FacultyCreateView(generics.CreateAPIView):
    """Yangi fakultet yaratish (faqat admin)."""
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fakultet yaratish (Admin)",
        operation_description="Yangi fakultet qo'shish — faqat admin uchun.",
        request_body=FacultySerializer,
        responses={201: FacultySerializer},
        tags=['Fakultetlar'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FacultyUpdateView(generics.UpdateAPIView):
    """Fakultetni yangilash (faqat admin)."""
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fakultetni yangilash (Admin)",
        request_body=FacultySerializer,
        responses={200: FacultySerializer},
        tags=['Fakultetlar'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fakultetni qisman yangilash (Admin)",
        request_body=FacultySerializer,
        responses={200: FacultySerializer},
        tags=['Fakultetlar'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class FacultyDeleteView(generics.DestroyAPIView):
    """Fakultetni o'chirish (faqat admin)."""
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Fakultetni o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Fakultetlar'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
