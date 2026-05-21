from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ─── Swagger API hujjatlash konfiguratsiyasi ──────────────────────────────────
api_info = openapi.Info(
    title="UniGuide API",
    default_version='v1',
    description=(
        "UniGuide loyihasi uchun REST API hujjatlari.\n\n"
        "**Autentifikatsiya:** JWT Bearer token ishlatiladi.\n"
        "Login qilib olingan `access` tokenni quyidagicha kiriting:\n"
        "`Bearer <access_token>`"
    ),
    terms_of_service="https://uniguide.uz/terms/",
    contact=openapi.Contact(email="support@uniguide.uz"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Accounts API
    path('api/v1/', include('accounts.urls', namespace='accounts')),

    # ─── Swagger UI va ReDoc ──────────────────────────────────────────────────
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# ─── Admin panel nomi ──────────────────────────────────────────────────────────
admin.site.site_header = "UniGuide Admin paneli"
admin.site.site_title = "UniGuide Portal"
admin.site.index_title = "Loyihani boshqarishga xush kelibsiz"