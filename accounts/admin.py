from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Ustunlar ro'yxatida nimalar ko'rinsin
    list_display = ['email', 'phone_number', 'is_staff', 'is_active']
    # Qidiruv maydoni
    search_fields = ['email', 'phone_number']
    # Saralash (ustun bosilganda)
    ordering = ['email']
    
    # Biz 'username'ni o'chirganimiz sababli filter_horizontal ichidagi eski guruhlarni tozalaymiz
    filter_horizontal = ('groups', 'user_permissions')

    # 1. Foydalanuvchi ma'lumotlarini TAHRIRLASH sahifasi (Bu yerda username umuman bo'lmasligi shart)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy ma\'lumotlar', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Huquq va Vazifalar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )

    # 2. Yangi foydalanuvchi QO'SHISH sahifasi
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active'),
        }),
    )

# Modelni qayta ro'yxatdan o'tkazamiz
admin.site.register(CustomUser, CustomUserAdmin)