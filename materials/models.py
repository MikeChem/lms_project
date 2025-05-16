from django.db import models
from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True, verbose_name='Превью')
    video_url = models.URLField(verbose_name='Ссылка на видео')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} → {self.course}'