from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwnerOrModeratorReadOnly  # ← добавлен IsOwnerOrModeratorReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Не модератор может создать
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Модератор или владелец
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrModeratorReadOnly]  # Удалить может только владелец
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязка к владельцу


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [~IsModerator & IsAuthenticated]  # Создание — не модератор
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        serializer.save(owner=self.request.user, course=course)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModeratorReadOnly]  # Редактирование и просмотр: владелец или модератор

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)  # Можно оставить, если хочешь обновлять владельца