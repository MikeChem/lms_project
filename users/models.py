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

    PAYMENT_STATUS_CHOICES = [
        ('created', 'Создано'),
        ('paid', 'Оплачено'),
        ('unpaid', 'Не оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс'
    )

    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )

    amount = models.PositiveIntegerField(
        verbose_name='Сумма (в центах)',
        help_text='Сумма в центах (например, 999 = $9.99)'
    )

    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Product ID'
    )

    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Price ID'
    )

    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Session ID'
    )

    payment_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату'
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='created',
        verbose_name='Статус платежа'
    )

    def __str__(self):
        return f"{self.user} - {self.amount / 100:.2f} USD ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'