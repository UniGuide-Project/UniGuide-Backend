from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """Yangi foydalanuvchi ro'yxatdan o'tkazish uchun serializer."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Parolni tasdiqlang",
        style={'input_type': 'password'},
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Foydalanuvchi kirishi uchun serializer."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Email yoki parol noto'g'ri!")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi faol emas!")

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Foydalanuvchi profilini ko'rish va yangilash uchun serializer."""

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'balance', 'is_active', 'date_joined']
        read_only_fields = ['id', 'email', 'balance', 'is_active', 'date_joined']


class ChangePasswordSerializer(serializers.Serializer):
    """Parolni o'zgartirish uchun serializer."""

    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        label="Yangi parolni tasdiqlang",
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Yangi parollar mos kelmadi!"})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Joriy parol noto'g'ri!")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Admin uchun foydalanuvchilar ro'yxati serializer."""

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'balance', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'date_joined']


from decimal import Decimal

class BalanceOperationSerializer(serializers.Serializer):
    """Balansga pul qo'shish yoki ayirish uchun serializer."""
    amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        required=True,
        min_value=Decimal('0.01'),
        error_messages={
            'min_value': "Qiymat 0 dan katta bo'lishi kerak."
        }
    )

