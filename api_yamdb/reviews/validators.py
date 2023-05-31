import re

from django.core.exceptions import ValidationError
from django.utils import timezone


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
    if re.search(r'^me$', value):
        raise ValidationError(
            ('Имя <me> служебное.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
