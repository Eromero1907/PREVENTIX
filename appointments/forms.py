from django import forms
from .models import Appointment
from .validators import validate_address

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label='Fecha',  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'})
    )
    time = forms.TimeField(
        input_formats=['%I:%M %p'], 
        label='Hora', 
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'})
    )
    address = forms.CharField(
        max_length=250,
        label='Dirección',
        validators=[validate_address],  # ← Agregamos la validación aquí
        widget=forms.TextInput(attrs={'placeholder': 'Cra 12 #34 - 56'})
    )
    doctor_name = forms.CharField(
        max_length=100,
        label='Nombre del médico',
        widget=forms.TextInput(attrs={'placeholder': 'Dr. Juan Pérez'})
    )

    class Meta:
        model = Appointment
        fields = ['title', 'date', 'time', 'description', 'address', 'doctor_name']
        labels = {
            'title': 'Título',
            'date': 'Fecha',
            'time': 'Hora',
            'description': 'Descripción',
            'address': 'Dirección',
            'doctor_name': 'Nombre del médico'
        }

class DireccionForm(forms.Form):
    direccion = forms.CharField(max_length=50, validators=[validate_address])
