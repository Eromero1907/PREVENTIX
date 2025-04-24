from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Prescription(models.Model):
    class MedicationForm(models.TextChoices):
        ORAL = 'Oral', 'Oral'
        INJECTION = 'Inyección', 'Inyección'
        TOPICAL = 'Tópico', 'Tópico'
        INHALED = 'Inhalado', 'Inhalado'
        OTHER = 'Otro', 'Otro'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)

    unit_per_dose = models.PositiveIntegerField(help_text="Cantidad por dosis (ej: 2 pastillas, 5 ml)")
    dosage_amount = models.FloatField(null=True, blank=True, help_text="Dosis numérica (ej: 500 mg, si aplica)")
    dosage_unit = models.CharField(max_length=20, null=True, blank=True, help_text="Unidad de dosis (ej: mg, ml)")

    interval_hours = models.PositiveIntegerField(help_text="Frecuencia en horas entre dosis (ej: cada 8 horas)")
    duration_days = models.PositiveIntegerField(help_text="Duración del tratamiento en días")

    start_date = models.DateField(default=timezone.now)
    administration_method = models.CharField(
        max_length=20,
        choices=MedicationForm.choices,
        default=MedicationForm.ORAL
    )

    restrictions = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration_days)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.interval_hours <= 0:
            raise ValidationError("El intervalo entre dosis debe ser mayor a cero horas.")

    def __str__(self):
        return f"{self.medication} ({self.unit_per_dose} unidad(es) cada {self.interval_hours} horas)"

class MedicalFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ahora usa settings.
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
