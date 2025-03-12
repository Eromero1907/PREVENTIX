from django.db import models

class Prescription(models.Model):
    MEDICATION_FORMS = [
        ('Oral', 'Oral'),
        ('Inyección', 'Inyección'),
        ('Tópico', 'Tópico'),
        ('Inhalado', 'Inhalado'),
        ('Otro', 'Otro'),
    ]

    medication = models.CharField(max_length=255)
    pills_per_dose = models.PositiveIntegerField()
    dosage_mg = models.PositiveIntegerField(null=True, blank=True)  # Opcional
    interval_hours = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    administration_method = models.CharField(max_length=20, choices=MEDICATION_FORMS, default='Oral')
    restrictions = models.TextField(blank=True, null=True)  # Ejemplo: "No tomar con alcohol"
    description = models.TextField(blank=True, null=True)  # Breve info sobre el medicamento

    def __str__(self):
        return f"{self.medication} ({self.pills_per_dose} pastilla(s) cada {self.interval_hours} horas)"
