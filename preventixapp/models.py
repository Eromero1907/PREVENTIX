from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

def validate_address(value):
    """
    Valida que la dirección siga el formato:
    Cra (número)(extensión) #(número)(extensión) - (número)
    Ejemplo: Cra 45A #67B - 10
    """
    print(f"Dirección recibida: '{value}'")
    value = value.strip(

    )
    pattern = r"^(Cra|Calle|Cl) \d+[A-Za-z]? #\d+[A-Za-z]? - \d+$"

    if not re.match(pattern, value):
        raise ValidationError("Formato de dirección inválido. Usa: Cra (número)(extensión) #(número)(extensión) - (número)")
    
class Usuario(models.Model):
    direccion = models.CharField(max_length=50, validators=[validate_address])
