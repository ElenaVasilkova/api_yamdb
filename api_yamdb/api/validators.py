from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

username_validator = UnicodeUsernameValidator()


def not_me_username_validator(value):
    if value.lower() == "me":
        raise ValidationError(
            "Имя 'me' не разрешено для использования."
        )
