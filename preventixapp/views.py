from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser
from datetime import datetime
from django.http import JsonResponse
from appointments.models import Appointment 
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime


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

def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'appointments': appointments})
