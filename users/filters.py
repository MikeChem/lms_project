import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    # Фильтрация по курсу
    course = django_filters.NumberFilter(field_name='course__id')
    # Фильтрация по уроку
    lesson = django_filters.NumberFilter(field_name='lesson__id')
    # Фильтрация по способу оплаты
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']