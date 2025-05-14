# preventixapp/forms.py
from django import forms
from .models import CustomUser
from datetime import date
from django.core.exceptions import ValidationError
from django import forms
from .models import CustomUser

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'id': 'id_profile_picture'}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and not picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Solo se permiten archivos .png, .jpg o .jpeg")
        return picture

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'phone_number',
            'direccion',
            'gender',
            'blood_type',
            'insurance',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return birth_date
