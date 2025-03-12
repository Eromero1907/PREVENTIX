import re
from django.core.exceptions import ValidationError

def validate_address(value):
    pattern = r"^(Cra|Calle|Cl) \d+[A-Za-z]? #\d+[A-Za-z]? - \d+$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Formato de dirección inválido. Usa: Cra (número) # (número) - (número)"
        )

