from rest_framework import viewsets, generics, status, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwnerOrModeratorReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.models import Course, Subscription
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import Http404

# ViewSet для курсов
from django.db.models import Count

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(lessons_count=Count('course'))
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Не модератор может создать
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrModeratorReadOnly]     # Модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrModeratorReadOnly]     # Удалить может только владелец
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязка к пользователю при создании


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


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModeratorReadOnly]  # Владелец или модератор


# APIView для подписки
class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Не указан course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_item = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Курс не найден"},
                status=status.HTTP_400_BAD_REQUEST  # ← Меняем сюда
            )

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)