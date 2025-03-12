from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'medication', 'pills_per_dose', 'dosage_mg', 'interval_hours',
            'duration_days', 'administration_method', 'restrictions', 'description'
        ]
        labels = {
            'medication': 'Medicamento',
            'pills_per_dose': 'Cantidad por toma (pastillas)',
            'dosage_mg': 'Dosis (mg) [Opcional]',
            'interval_hours': 'Cada cuántas horas',
            'duration_days': 'Días de duración',
            'administration_method': 'Forma de administración',
            'restrictions': 'Restricciones',
            'description': 'Descripción breve',
        }
