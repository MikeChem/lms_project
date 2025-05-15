from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from .views import SubscriptionAPIView
# Создаём роутер для ViewSet'а (курсов)
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # Подключаем маршруты от роутера
    path('', include(router.urls)),

    # Маршруты для уроков (Generic-классы)
    path('lessons/<int:course_id>/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
]