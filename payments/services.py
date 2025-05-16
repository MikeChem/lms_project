import stripe
from django.conf import settings
from users.models import Payment


# Подключаемся к Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """
    Создаёт продукт в Stripe на основе курса
    """
    product = stripe.Product.create(
        name=course.title,
        description=course.description or "Курс обучения",
        images=[course.preview.url] if course.preview else []
    )
    return product


def create_stripe_price(amount, product_id):
    """
    Создаёт цену в Stripe (в центах)
    """
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # конвертируем в центы
        currency="usd",
        product=product_id,
    )
    return price


def create_checkout_session(price_id):
    """
    Создаёт сессию оплаты в Stripe и возвращает ссылку
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=settings.SUCCESS_URL,
        cancel_url=settings.CANCEL_URL,
    )
    return session.url, session.id


def get_payment(payment_id):
    """
    Получает объект оплаты из нашей БД
    """
    try:
        return Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return None


def retrieve_stripe_session(session_id):
    """
    Возвращает статус сессии Stripe
    """
    return stripe.CheckoutSession.retrieve(session_id)