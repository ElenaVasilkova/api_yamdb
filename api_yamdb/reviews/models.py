from django.db import models

from .validators import validate_year


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
