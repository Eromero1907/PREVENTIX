from django.shortcuts import render, redirect
from django.utils.dateformat import format as date_format
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser
from .utils import get_forgotten_specialties
from appointments.ml_model import recommend_appointments
from appointments.models import Appointment 
import json
from .forms import ProfilePictureForm, ProfileInfoForm
from datetime import date

User = get_user_model()

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Buscar el usuario por email
            user = User.objects.get(email=email)
            # Autenticar usando el username del usuario
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirige al dashboard después del login exitoso
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
        except User.DoesNotExist:
            messages.error(request, 'No existe una cuenta con este correo.')

    return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Solo correo electrónico
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Asegúrate de que 'home' esté definido en tus URLs
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        
        # Verificar si el número de teléfono ya existe
        if CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Este número de teléfono ya está registrado.')
            return redirect('register')  # Asegúrate de que 'register' sea el nombre correcto de la URL

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return redirect('register')

        # Guardar el usuario si no hay conflictos
        user = CustomUser.objects.create_user(
            username=email,
            phone_number=phone,
            email=email,
            password=request.POST['password']
        )
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')

@login_required
def dashboard(request):
    # Obtener estadísticas y especialidades olvidadas
    stats = (
        Appointment.objects
        .filter(user=request.user)
        .exclude(specialty__isnull=True)
        .exclude(specialty='')
        .values('specialty')
        .annotate(count=Count('specialty'))
        .order_by('-count')
    )

    labels = [item['specialty'] for item in stats]
    counts = [item['count'] for item in stats]

    forgotten = get_forgotten_specialties(request.user)
    for item in forgotten:
        item['last_date'] = date_format(item['last_date'], 'Y-m-d')

    # Obtener citas recomendadas para el usuario
    recommended_appointments = recommend_appointments(request.user.id)

    return render(request, 'dashboard.html', {
        'labels': json.dumps(labels),
        'counts': json.dumps(counts),
        'forgotten_specialties': forgotten,
        'recommended_appointments': recommended_appointments.to_dict('records'),  # Convierte el DataFrame a dict
    })

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        if 'profile_picture' in request.POST:
            picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user)
            info_form = ProfileInfoForm(instance=user)
            if picture_form.is_valid():
                picture_form.save()
                messages.success(request, 'Foto de perfil actualizada correctamente.')
                return redirect('profile')
        else:
            info_form = ProfileInfoForm(request.POST, instance=user)
            picture_form = ProfilePictureForm(instance=user)

            if info_form.is_valid():
                info_form.save()  # 💡 Aquí guardamos los datos en el usuario
                messages.success(request, 'Información actualizada correctamente.')
                return redirect('profile')
            else:
                print(info_form.errors)  # Para ver si hay errores al validar

    else:
        picture_form = ProfilePictureForm(instance=user)
        info_form = ProfileInfoForm(instance=user)

    return render(request, 'profile.html', {
        'picture_form': picture_form,
        'info_form': info_form,
    })

