from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# Роутер для ViewSet'ов
router = DefaultRouter()
# Добавляй ViewSet'ы сюда через router.register(...)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/materials/', include('materials.urls')),
    path('api/payments/', include(router.urls)),
# OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]