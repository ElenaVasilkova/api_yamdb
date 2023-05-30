import datetime as dt
import re

from django.core.exceptions import ValidationError


def validate_year(value):
    if dt.date.today().year < value:
        raise ValidationError('Wrong year!')
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя <me> служебное.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
