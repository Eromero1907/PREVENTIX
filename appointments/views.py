from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/list.html', {'appointments': appointments})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirige a la lista de citas
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/edit_appointment.html', {'form': form})


def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigir al dashboard después de crear la cita
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/create_appointment.html', {'form': form})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        appointment.delete()
        return redirect('appointment_list')  # Redirige a la lista de citas después de eliminar

    return render(request, 'appointments/delete_appointment.html', {'appointment': appointment})
