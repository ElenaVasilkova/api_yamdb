from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


CHAR_LIMIT = 20


class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=256)
    slug = models.SlugField(
        verbose_name='id', unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Genre', max_length=256)
    slug = models.SlugField(
        verbose_name='id', unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Name', max_length=256
    )
    year = models.IntegerField(
        verbose_name='Data', validators=[validate_year], db_index=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Category', related_name='titles',
        on_delete=models.SET_NULL, null=True, db_index=True
    )
    description = models.TextField(
        verbose_name='Description', null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр', db_index=True
    )
    rating = models.IntegerField(
        verbose_name='Rating', null=True, default=None, db_index=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Title'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Genre'
    )

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    text = models.CharField(
        max_length=200
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:CHAR_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.CharField(
        'текст комментария',
        max_length=200
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:CHAR_LIMIT]
