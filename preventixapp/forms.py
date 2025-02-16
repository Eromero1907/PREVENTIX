from django import forms
from .models import Appointment
from .validators import validate_address

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'})
    )
    time = forms.TimeField(
        input_formats=['%I:%M %p'],  
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'})
    )
    address = forms.CharField(
        max_length=250,
        validators=[validate_address],  # ← Agregamos la validación aquí
        widget=forms.TextInput(attrs={'placeholder': 'Cra 12 #34 - 56'})
    )
    doctor_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Dr. Juan Pérez'})
    )

    class Meta:
        model = Appointment
        fields = ['title', 'date', 'time', 'description', 'address', 'doctor_name']

class DireccionForm(forms.Form):
    direccion = forms.CharField(max_length=50, validators=[validate_address])
