from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Payment


# Сериализатор для отображения и редактирования пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']
        read_only_fields = ['id']


from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'city', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', None),
            city=validated_data.get('city', None),
            avatar=validated_data.get('avatar', None)  # Может быть None
        )
        return user


# Сериализатор для входа (логин через email и пароль)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Неверные учетные данные")
        else:
            raise serializers.ValidationError("Необходимо указать email и пароль")

        return data


# Сериализатор платежей (можно оставить как есть)
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
