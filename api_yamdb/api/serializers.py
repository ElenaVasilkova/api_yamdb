from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import not_me_username_validator, username_validator


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')


class NotAdminSerializer(UsersSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[not_me_username_validator, username_validator],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, data):
        if not User.objects.filter(
            username=data.get("username"), email=data.get("email")
        ).exists():
            if User.objects.filter(username=data.get("username")):
                raise serializers.ValidationError(
                    "Пользователь с таким username уже существует"
                )

            if User.objects.filter(email=data.get("email")):
                raise serializers.ValidationError(
                    "Пользователь с таким Email уже существует"
                )

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        # Пересоздаем запись в базе если точно такой же пользователь уже есть
        User.objects.filter(username=username, email=email).delete()
        return User.objects.create(email=email, username=username)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        now = timezone.now().year
        if value > now:
            raise ValidationError(
                f'{value} не может быть больше {now}!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Отзыв уже существует.')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        title_id = self.context.get('view').kwargs.get('title_id')
        review_id = self.context.get('view').kwargs.get('review_id')

        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, title=title, id=review_id)

        validated_data['author'] = self.context['request'].user
        validated_data['review'] = review

        return super().create(validated_data)
