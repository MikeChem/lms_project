from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager  # ← будем использовать кастомный менеджер


class User(AbstractUser):
    username = None  # Отключаем username
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Теперь не нужно указывать обязательные поля

    objects = CustomUserManager()  # Используем кастомный менеджер

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(
        'materials.Course',  # ← Указываем строкой для избежания циклического импорта
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        'materials.Lesson',  # ← Указываем строкой
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='TRANSFER',
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'