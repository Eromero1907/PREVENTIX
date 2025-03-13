from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from .models import Appointment
from django.contrib.auth.decorators import login_required

# Lista solo las citas del usuario autenticado
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)  # Filtrar por usuario
    return render(request, 'appointments/list.html', {'appointments': appointments})

# Edita solo citas del usuario autenticado
@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)  # Verifica que la cita pertenezca al usuario

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirige a la lista de citas
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/edit_appointment.html', {'form': form})

# Crea una cita asignándola al usuario autenticado
@login_required
def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Asigna la cita al usuario autenticado
            appointment.save()
            return redirect('dashboard')  # Redirigir al dashboard después de crear la cita
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/create_appointment.html', {'form': form})

# Solo permite eliminar citas del usuario autenticado
@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)  # Verifica que la cita pertenezca al usuario

    if request.method == "POST":
        appointment.delete()
        return redirect('appointment_list')  # Redirige a la lista de citas después de eliminar

    return render(request, 'appointments/delete_appointment.html', {'appointment': appointment})
