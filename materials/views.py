# materials/views.py

from rest_framework import viewsets, generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payment
from users.permissions import IsModerator, IsOwnerOrModeratorReadOnly
from django.db.models import Count
from materials.tasks import check_and_notify_subscribers


# ViewSet для курсов
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(lessons_count=Count('lessons'))
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator & IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrModeratorReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrModeratorReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Создание курса с привязкой к владельцу"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Обновление курса + рассылка подписчикам"""
        course = serializer.save()
        check_and_notify_subscribers.delay(course.id)

# Generic для уроков
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [~IsModerator & IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id') or self.request.data.get('course')

        if not course_id:
            raise serializers.ValidationError({"course": "Не указан course"})

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course": "Курс не найден"})

        serializer.save(owner=self.request.user, course=course)


# Generic для редактирования урока
class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModeratorReadOnly]  # Владелец или модератор

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Подписка или отписка от курса
        """
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Не указан course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Курс не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, есть ли такая подписка
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)