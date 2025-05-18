from celery import shared_task
from django.core.mail import send_mail
from materials.models import Course, Subscription
from django.conf import settings


@shared_task
def check_and_notify_subscribers(course_id):
    """
    Рассылает подписчикам сообщение о том, что курс был обновлён
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    subscribers = Subscription.objects.filter(course=course, user__is_active=True)

    for subscriber in subscribers:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Привет!\n\nКурс '{course.title}' был обновлён. Посмотрите новые уроки и материалы.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email],
            fail_silently=False,
        )

    print(f"Уведомлено {subscribers.count()} подписчик(ов) о курсе '{course.title}'")