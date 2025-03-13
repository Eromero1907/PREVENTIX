from django.db import models
from django.conf import settings

class Prescription(models.Model):
    MEDICATION_FORMS = [
        ('Oral', 'Oral'),
        ('Inyección', 'Inyección'),
        ('Tópico', 'Tópico'),
        ('Inhalado', 'Inhalado'),
        ('Otro', 'Otro'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ahora usa settings.
    medication = models.CharField(max_length=255)
    pills_per_dose = models.PositiveIntegerField()
    dosage_mg = models.PositiveIntegerField(null=True, blank=True)
    interval_hours = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    administration_method = models.CharField(max_length=20, choices=MEDICATION_FORMS, default='Oral')
    restrictions = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medication} ({self.pills_per_dose} pastilla(s) cada {self.interval_hours} horas)"

class MedicalFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ahora usa settings.
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
