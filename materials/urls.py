# materials/urls.py
from django.urls import path
from . import views

app_name = 'materials'  # Namespace для URL

urlpatterns = [
    # Courses
    path('courses/', views.CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
    path('courses/<int:pk>/', views.CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='course-detail'),

    # Lessons
    path('lessons/', views.LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),

    # Subscriptions
    path('subscribe/', views.SubscriptionAPIView.as_view(), name='subscription-create'),
]