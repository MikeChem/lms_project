from rest_framework import viewsets, permissions, generics, serializers
from django.contrib.auth import authenticate
from .models import User, Payment
from .serializers import UserSerializer, RegisterSerializer, PaymentSerializer
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# ========== JWT Авторизация ==========
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ========== Регистрация пользователя ==========
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ========== CRUD для пользователей ==========
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


# ========== CRUD для платежей с разграничением прав ==========
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение: Администратор может всё, остальные — только чтение.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для управления платежами.
    Поддерживает:
    - Фильтрацию по курсу, уроку и способу оплаты
    - Сортировку по дате оплаты
    - Разграничение прав: только администратор может редактировать данные
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    # Только авторизованные пользователи могут работать с этим API
    permission_classes = [permissions.IsAuthenticated]

    # Опционально: разные права в зависимости от действия
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]