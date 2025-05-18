import os
from celery import Celery
from django.conf import settings

# Установка переменной окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра Celery
app = Celery('lms_project')

# Использовать настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автообнаружение задач
app.autodiscover_tasks()

# Явное указание timezone из настроек Django
app.conf.enable_utc = False
app.conf.timezone = settings.TIME_ZONE