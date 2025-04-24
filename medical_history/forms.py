from django import forms
from .models import Prescription
from .models import MedicalFile

class MedicalFileForm(forms.ModelForm):
    class Meta:
        model = MedicalFile
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'medication', 'unit_per_dose', 'dosage_amount', 'dosage_unit',
            'interval_hours', 'duration_days', 'start_date',
            'administration_method', 'restrictions', 'description'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
