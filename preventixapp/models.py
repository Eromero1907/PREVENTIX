from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
    
class Usuario(models.Model):
    direccion = models.CharField(max_length=50)

class CustomUser(AbstractUser):
    # Campos obligatorios (además de username y password heredados de AbstractUser)
    phone_number = models.CharField(max_length=15, unique=True)  # Obligatorio
    direccion = models.CharField(max_length=50)  # Obligatorio

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
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='images/default_profile.png')

    def __str__(self):
        return self.username
