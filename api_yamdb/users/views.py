from rest_framework import filters, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .serializers import (
    MeUpdateSerialier, UserSerializer, SignUpSerializer, TokenSerializer
)
from users.models import User
from .permissions import IsAdmin, IsAdminOrReadOnly, AllowAny


class UserViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            user, created = User.objects.get_or_create(**serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeViewSet(RetrieveUpdateAPIView):
    serializer_class = MeUpdateSerialier
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user


class TokenViewSet(CreateAPIView):
    permission_classes = [AllowAny]

    def get_tokens_for_user(self, user):
        """
        Генерация токена для доступа к API.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token)
        }

    def token(self, request):
        """
        Получение JWT-токена в обмен на username и confirmation_code.
        """
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data['username']
            confirmation_code = serializer.initial_data['confirmation_code']

            if not username or not confirmation_code:
                return Response(
                    {"error": "Username and confirmation code are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not User.objects.filter(username=username).exists():
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
                user = get_object_or_404(User, username=username)

            if user.confirmation_code == confirmation_code:
                token = self.get_tokens_for_user(user)
                return Response(token, status=status.HTTP_200_OK)
            return Response('Invalid confirmation_code',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SignUpViewSet(CreateAPIView):
    permission_classes = [AllowAny]

    def signup(self, request):
        """
        Регистрация пользователя и отправка кода подтверждения на его email.
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token_generator = PasswordResetTokenGenerator()
            user = User.objects.get(
                username=serializer.initial_data['username'])
            user.confirmation_code = token_generator.make_token(user=user)
            user.save()
            try:
                self.send_code(user.email, user.confirmation_code)
            except Exception:
                print("Ошибка отправки email с кодом подтверждения")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def send_code(self, recipient, confirmation_code):
        """
        Отправка кода подтверждения на email пользователя.
        """
        status = send_mail(
            'Код подтверждения',
            f'Здравствуйте, используйте этот код подтверждения '
            f'{confirmation_code} для получения токена.',
            'noreply@yamdb.com',
            [f'{recipient}'],
            fail_silently=False,
        )
        return status


'''
class APIUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
        )
'''
