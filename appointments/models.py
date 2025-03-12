from django.db import models
import re
from django.core.exceptions import ValidationError

# Create your models here.

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

class Appointment(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    specialty = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255)  # Nuevo campo para el nombre del doctor
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, validators=[validate_address])  # Dirección con validación

    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"