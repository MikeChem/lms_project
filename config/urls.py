from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('materials.urls')),  # Подключаем маршруты из materials/urls.py
]

