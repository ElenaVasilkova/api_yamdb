from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\z'


class User(AbstractUser):
    """
    Полнофункциональная модель пользователя.
    """

    description = models.TextField(
        'Детальная информация о пользователе.'
    )
    username_validator = MyValidator()
    username = models.CharField(
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
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        validators=[validators.EmailValidator(
            message="Неверный адрес электронной почты"
        )],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    role = models.TextField(
        verbose_name='Права доступа',
        help_text=(
            'Администратор, модератор или пользователь. По умолчанию user.'
        ),
        blank=True,
        choices=Role.choices,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Confirmation code',
        default='00000000'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('username', 'email')
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_user"
            )
        ]

    def __str__(self):
        return self.username
