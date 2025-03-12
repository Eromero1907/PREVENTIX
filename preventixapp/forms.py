from django import forms
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
