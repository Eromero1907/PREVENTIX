import re
from django.core.exceptions import ValidationError

def validate_address(value):
    # Esta expresión regular permite formatos comunes como:
    # "Cra 12 #34 - 56", "Calle 45 #123 - 78 Apto 304", etc.
    pattern = r"^(Cra|Calle|Cl)\s?\d+[A-Za-z]?\s?#\s?\d+[A-Za-z]?\s?-\s?\d+.*$"
    if not re.match(pattern, value.strip()):
        raise ValidationError(
            "Formato de dirección inválido. Usa algo como: 'Cra 12 #34 - 56'"
        )

