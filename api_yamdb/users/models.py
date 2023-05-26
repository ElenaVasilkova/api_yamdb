from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\z'


class User(AbstractUser):
    """Полнофункциональная модель пользователя."""

    description = models.TextField(
        'Детальная информация о пользователе.'
    )
    username_validator = MyValidator()
    username = models.CharField(
        related_name='username',
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters,'
            'digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    email = models.EmailField(
        related_name='email',
        verbose_name='Email',
        max_length=254,
    )
    first_name = models.CharField(
        related_name='first_name',
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        related_name='last_name',
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        related_name='bio',
        verbose_name='Биография',
        blank=True
    )

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    role = models.TextField(
        related_name='role',
        verbose_name='Роль пользователя',
        help_text=(
            'Администратор, модератор или пользователь. По умолчанию user.'
        ),
        blank=True,
        choices=Role.choices,
        default='user'
    )

    class Meta:
        unique_together = ('username', 'email')

    def __str__(self):
        return self.username
