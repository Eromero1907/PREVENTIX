from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core.exceptions import ValidationError
from datetime import date

def validate_address(value):
    """
    Valida el formato de direcciones de manera flexible:
    - Permite espacios adicionales o faltantes
    - Acepta distintas formas de escribir (Calle, Cra, Carrera, Tv, Transversal, Diagonal)
    - Acepta complementos: sur, norte, este, oeste
    - No es sensible a mayúsculas o minúsculas
    - Ejemplos válidos:
      Calle 27 sur #25B - 76
      cra50 norte - 15
      transversal45 sur #14a - 10
      Diagonal 32a este #45b-21
    """
    # Remover espacios en blanco al inicio y al final
    value = value.strip()

    # Expresión regular que acepta múltiples formatos y es insensible a mayúsculas
    pattern = r"^(calle|cra|carrera|tv|transversal|diagonal)\s*\d+[a-zA-Z]?\s*(sur|norte|este|oeste)?\s*(?:#\s*\d+[a-zA-Z]?)?\s*-\s*\d+$"
    
    if not re.match(pattern, value, re.IGNORECASE):
        raise ValidationError(
            "Formato de dirección inválido. Ejemplos válidos: 'Calle 27 sur #25B - 76', 'cra50 norte - 15', 'transversal45 sur #14a - 10'"
        )
    
class Usuario(models.Model):
    direccion = models.CharField(max_length=50, validators=[validate_address])

class CustomUser(AbstractUser):
    # Campos obligatorios (además de username y password heredados de AbstractUser)
    phone_number = models.CharField(max_length=15, unique=True)  # Obligatorio
    direccion = models.CharField(max_length=50, validators=[validate_address])  # Obligatorio

    # Campos opcionales
    birth_date = models.DateField(null=True, blank=True)
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return (
                today.year
                - self.birth_date.year
                - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            )
        return None
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        blank=True
    )
    blood_type = models.CharField(max_length=3, blank=True)
    insurance = models.CharField("EPS / Aseguradora", max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
