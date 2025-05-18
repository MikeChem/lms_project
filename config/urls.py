from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Роутер для ViewSet'ов
router = DefaultRouter()
# Добавляй ViewSet'ы сюда через router.register(...)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/materials/', include('materials.urls')),
    path('api/payments/', include(router.urls)),
]