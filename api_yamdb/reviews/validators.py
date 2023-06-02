import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

username_validator = UnicodeUsernameValidator()


def validate_year(value):
    """
    Проверка на корректность года
    выхода произведения.
    """

    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}!'
        )


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            "Имя 'me' не разрешено для использования."
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
