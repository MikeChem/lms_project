from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson, Subscription
from users.models import User
from django.contrib.auth.models import Group

class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )

        # Создаем курс и урок для тестирования
        self.course = Course.objects.create(title='Python Basic', owner=self.admin)
        self.lesson = Lesson.objects.create(
            title='Введение в Python',
            course=self.course,
            video_url='https://youtube.com/watch?v=abc123 ',
            owner=self.admin
        )
        self.client.force_authenticate(user=self.user)


    def test_lesson_list(self):
        """Проверяет, что список уроков доступен"""
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_lesson_create(self):
        """Проверяет, что можно создать урок"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-list')
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=new_video'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CourseAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user)

    def test_course_list(self):
        """Проверяет, что список курсов доступен"""
        url = reverse('materials:course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_create(self):
        """Проверяет, что можно создать курс"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:course-list')
        data = {
            'title': 'Новый курс',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )

        # Создаем курс для подписки
        self.course = Course.objects.create(title='Python Pro', owner=self.admin)

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Проверяет, что пользователь может подписаться на курс"""
        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.id}  # Send course_id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_unsubscribe_from_course(self):
        """Проверяет, что пользователь может отписаться от курса"""
        # Create subscription first
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.id}  # Send course_id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')