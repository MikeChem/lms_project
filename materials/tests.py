from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Subscription
from users.models import User
from django.contrib.auth.models import Group
from rest_framework import status

class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей БЕЗ username
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='password123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )

        # Назначаем группу "Модератор"
        group, created = Group.objects.get_or_create(name='Модератор')
        self.moderator.groups.add(group)

        # Создаем курс и урок для тестирования
        self.course = Course.objects.create(title='Python Basic', owner=self.admin)
        self.lesson = Lesson.objects.create(
            title='Введение в Python',
            course=self.course,
            video_url='https://youtube.com/watch?v=abc123 ',
            owner=self.admin
        )

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        """Проверяет, что список уроков доступен"""
        response = self.client.get('/api/materials/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        """Проверяет, что только не модератор может создавать уроки"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=new_video '
        }
        response = self.client.post('/api/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_moderator_cannot_create_lesson(self):
        """Модератор не может создать урок"""
        self.client.force_authenticate(user=self.moderator)
        data = {
            'title': 'Не должен быть создан',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=abc123 '
        }
        response = self.client.post('/api/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_by_owner(self):
        """Владелец может обновлять урок"""
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'Обновлённое название'}
        response = self.client.patch(f'/api/materials/lessons/{self.lesson.id}/', data)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновлённое название')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_by_owner(self):
        """Владелец может удалить урок"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/materials/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

# Тесты подписки на курс
class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.course = Course.objects.create(title='Python Basic', description='Курс по Python')

    def test_subscribe_to_course(self):
        """Подписка на курс работает корректно"""
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post('/api/materials/subscribe/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

    def test_unsubscribe_from_course(self):
        """Отписка от курса работает корректно"""
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'course_id': self.course.id}
        response = self.client.post('/api/materials/subscribe/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')

    def test_invalid_course_subscription(self):
        """Ошибка при попытке подписаться на несуществующий курс"""
        self.client.force_authenticate(user=self.user)
        data = {'course_id': 9999}
        response = self.client.post('/api/materials/subscribe/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)