from rest_framework import serializers

from .models import User
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        read_only_fields = ('username', 'email', 'role',)
        lookup_field = 'username'

    def create(self, validated_data):
        if self.validated_data['username'] == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать это имя'
            )
        return User.objects.create(**validated_data)


class MeUpdateSerialier(UserSerializer):
    """
    Сериализатор ...
    """
    class Meta:
        model = User
        fields = ('role',)
        read_only_fields = ('id', 'role',)
        lookup_field = 'username'


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор получения JWT-токена.
    """
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор формы регистрации.
    """
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')
