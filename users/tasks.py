from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta


User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей, которые не заходили больше 30 дней
    """
    month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    print(f"Было заблокировано {count} пользователей")
    return count