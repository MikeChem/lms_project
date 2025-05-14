from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/materials/', include('materials.urls')),
    path('api/payments/', include(router.urls)),
]

