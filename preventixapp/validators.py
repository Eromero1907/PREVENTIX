import re
from django.core.exceptions import ValidationError

def validate_address(value):
    pattern = r'^Cra\s*\d+\s*#\s*\d+\s*-\s*\d+$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Formato de dirección inválido. Usa: Cra (número) # (número) - (número)"
        )

