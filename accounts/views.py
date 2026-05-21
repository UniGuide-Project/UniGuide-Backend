from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    UserListSerializer,
    BalanceOperationSerializer,
)


def get_tokens_for_user(user):
    """Foydalanuvchi uchun JWT tokenlarni yaratish."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish.

    Email, parol va ixtiyoriy ism/familiya/telefon raqami bilan yangi account yaratadi.
    Muvaffaqiyatli ro'yxatdan o'tgandan so'ng JWT tokenlar qaytariladi.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Ro'yxatdan o'tish",
        operation_description="Yangi foydalanuvchi yaratish va JWT token olish.",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="Muvaffaqiyatli ro'yxatdan o'tildi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: "Noto'g'ri ma'lumotlar",
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    'message': "Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                    'user': UserProfileSerializer(user).data,
                    'tokens': tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Tizimga kirish — JWT token olish.

    Email va parol orqali tizimga kirib, access va refresh tokenlarni oladi.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Tizimga kirish",
        operation_description="Email va parol orqali kirish va JWT token olish.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Muvaffaqiyatli kirildi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: "Noto'g'ri email yoki parol",
        },
        tags=['Auth'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    'message': "Tizimga muvaffaqiyatli kirdingiz!",
                    'user': UserProfileSerializer(user).data,
                    'tokens': tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Tizimdan chiqish — refresh tokenni bekor qilish.

    Refresh tokenni blacklistga qo'shib, foydalanuvchini tizimdan chiqaradi.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Tizimdan chiqish",
        operation_description="Refresh tokenni bekor qilib tizimdan chiqish.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh token",
                ),
            },
        ),
        responses={
            200: "Muvaffaqiyatli chiqildi",
            400: "Token noto'g'ri yoki allaqachon bekor qilingan",
        },
        tags=['Auth'],
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': "Refresh token talab qilinadi!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': "Tizimdan muvaffaqiyatli chiqdingiz!"},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {'error': "Token noto'g'ri yoki muddati o'tgan!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    """
    Foydalanuvchi profili — ko'rish va yangilash.

    GET: Joriy foydalanuvchi ma'lumotlarini olish.
    PUT/PATCH: Foydalanuvchi ma'lumotlarini yangilash.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Profil ma'lumotlarini olish",
        operation_description="Joriy foydalanuvchining profil ma'lumotlari.",
        responses={200: UserProfileSerializer},
        tags=['Profile'],
    )
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Profilni to'liq yangilash",
        operation_description="Foydalanuvchi profilini PUT orqali yangilash.",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer, 400: "Noto'g'ri ma'lumotlar"},
        tags=['Profile'],
    )
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Profilni qisman yangilash",
        operation_description="Foydalanuvchi profilini PATCH orqali qisman yangilash.",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer, 400: "Noto'g'ri ma'lumotlar"},
        tags=['Profile'],
    )
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Parolni o'zgartirish.

    Joriy parolni tekshirib, yangi parol o'rnatadi.
    Keyin yangi JWT tokenlar qaytariladi.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Parolni o'zgartirish",
        operation_description="Joriy parolni tekshirib, yangi parol belgilash.",
        request_body=ChangePasswordSerializer,
        responses={
            200: "Parol muvaffaqiyatli o'zgartirildi",
            400: "Noto'g'ri ma'lumotlar",
        },
        tags=['Profile'],
    )
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Yangi token berish
            tokens = get_tokens_for_user(request.user)
            return Response(
                {
                    'message': "Parol muvaffaqiyatli o'zgartirildi!",
                    'tokens': tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    Barcha foydalanuvchilar ro'yxati (faqat admin uchun).

    Tizimda ro'yxatdan o'tgan barcha foydalanuvchilarni ko'rish.
    Faqat admin huquqiga ega foydalanuvchilar uchun.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Foydalanuvchilar ro'yxati (Admin)",
        operation_description="Barcha foydalanuvchilarni ko'rish — faqat admin uchun.",
        responses={200: UserListSerializer(many=True)},
        tags=['Admin'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta foydalanuvchi — ko'rish, yangilash, o'chirish (faqat admin uchun).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Foydalanuvchi ma'lumotlari (Admin)",
        operation_description="ID orqali foydalanuvchi ma'lumotlarini olish.",
        responses={200: UserListSerializer},
        tags=['Admin'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Foydalanuvchini yangilash (Admin)",
        request_body=UserListSerializer,
        responses={200: UserListSerializer},
        tags=['Admin'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Foydalanuvchini qisman yangilash (Admin)",
        request_body=UserListSerializer,
        responses={200: UserListSerializer},
        tags=['Admin'],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Foydalanuvchini o'chirish (Admin)",
        responses={204: "Muvaffaqiyatli o'chirildi"},
        tags=['Admin'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AddBalanceView(APIView):
    """
    Foydalanuvchi balansiga pul qo'shish.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Balansga pul qo'shish",
        operation_description="Joriy foydalanuvchi balansini ko'paytirish.",
        request_body=BalanceOperationSerializer,
        responses={
            200: openapi.Response(
                description="Muvaffaqiyatli",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            ),
            400: "Noto'g'ri ma'lumotlar",
        },
        tags=['Profile'],
    )
    def post(self, request):
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            request.user.balance += amount
            request.user.save()
            return Response(
                {
                    "message": "Balans muvaffaqiyatli to'ldirildi.",
                    "balance": request.user.balance
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtractBalanceView(APIView):
    """
    Foydalanuvchi balansidan pul ayirish.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Balansdan pul ayirish",
        operation_description="Joriy foydalanuvchi balansidan pul yechish (masalan test yechish uchun).",
        request_body=BalanceOperationSerializer,
        responses={
            200: openapi.Response(
                description="Muvaffaqiyatli",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            ),
            400: "Noto'g'ri ma'lumotlar yoki mablag' yetarli emas",
        },
        tags=['Profile'],
    )
    def post(self, request):
        serializer = BalanceOperationSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            if request.user.balance < amount:
                return Response(
                    {"error": "Hisobda yetarli mablag' mavjud emas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            request.user.balance -= amount
            request.user.save()
            return Response(
                {
                    "message": "Balansdan muvaffaqiyatli yechib olindi.",
                    "balance": request.user.balance
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

