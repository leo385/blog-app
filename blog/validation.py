import re
from django.core.exceptions import ValidationError

def validate_only_letters(value):
    if not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError("Pole moze zawierac tylko litery od a-z lub A-Z")
