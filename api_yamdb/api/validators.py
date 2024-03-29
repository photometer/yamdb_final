from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.now().year
    if current_year < value:
        raise ValidationError(f'{value} - значение больше текущего года.'
                              'Введите правильный год выпуска')
