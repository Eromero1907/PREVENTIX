from django import forms
from .models import Appointment
from .validators import validate_address

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label='Fecha',
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY', 'class': 'form-control'})
    )
    time = forms.TimeField(
        input_formats=['%I:%M %p'],
        label='Hora',
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM', 'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=250,
        label='Dirección',
        validators=[validate_address],
        widget=forms.TextInput(attrs={'placeholder': 'Cra 12 #34 - 56', 'class': 'form-control'})
    )
    doctor_name = forms.CharField(
        max_length=100,
        label='Nombre del médico',
        widget=forms.TextInput(attrs={'placeholder': 'Dr. Juan Pérez', 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['title', 'date', 'time', 'specialty', 'description', 'address', 'doctor_name']
        labels = {
            'title': 'Título',
            'date': 'Fecha',
            'time': 'Hora',
            'specialty': 'Especialidad',
            'description': 'Descripción',
            'address': 'Dirección',
            'doctor_name': 'Nombre del médico'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DireccionForm(forms.Form):
    direccion = forms.CharField(max_length=50, validators=[validate_address])
