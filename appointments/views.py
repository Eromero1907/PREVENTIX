from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from appointments.templatetags.custom_filters import add_class

# Lista solo las citas del usuario autenticado
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)  # Filtrar por usuario
    return render(request, 'appointments/list.html', {'appointments': appointments})

# Edita solo citas del usuario autenticado
@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)

    # Lista completa de especialidades posibles
    all_specialties = [
        'Odontología', 'Vacunación', 'Chequeo general', 'Dermatología', 'Oftalmología',
        'Cardiología', 'Ginecología', 'Urología', 'Pediatría', 'Otorrinolaringología',
        'Medicina interna', 'Endocrinología', 'Nutrición', 'Psicología', 'Psiquiatría',
        'Neumología', 'Fisioterapia', 'Rehabilitación', 'Neurología', 'Revisión postoperatoria',
        'Análisis de laboratorio', 'Control de peso', 'Revisión de medicamentos',
        'Consulta virtual', 'Medicina del deporte'
    ]

    # Obtener especialidades más frecuentes del usuario
    top_specialties = (
        Appointment.objects.filter(user=request.user)
        .values('specialty')
        .annotate(count=Count('specialty'))
        .order_by('-count')
        .values_list('specialty', flat=True)
    )

    frequent = [s for s in top_specialties if s in all_specialties]
    others = [s for s in all_specialties if s not in frequent]

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirige a la lista de citas
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {
        'form': form,
        'frequent': frequent,
        'others': others
    })

# Crea una cita asignándola al usuario autenticado

@login_required
def create_appointment(request):
    user = request.user

    all_specialties = [
        'Odontología', 'Vacunación', 'Chequeo general', 'Dermatología', 'Oftalmología',
        'Cardiología', 'Ginecología', 'Urología', 'Pediatría', 'Otorrinolaringología',
        'Medicina interna', 'Endocrinología', 'Nutrición', 'Psicología', 'Psiquiatría',
        'Neumología', 'Fisioterapia', 'Rehabilitación', 'Neurología', 'Revisión postoperatoria',
        'Análisis de laboratorio', 'Control de peso', 'Revisión de medicamentos',
        'Consulta virtual', 'Medicina del deporte'
    ]

    top_specialties = (
        Appointment.objects.filter(user=user)
        .values('specialty')
        .annotate(count=Count('specialty'))
        .order_by('-count')
        .values_list('specialty', flat=True)
    )

    frequent = [s for s in top_specialties if s in all_specialties]
    others = [s for s in all_specialties if s not in frequent]
    specialty_choices = [(s, s) for s in frequent + others]

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        form.fields['specialty'].choices = specialty_choices

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = user
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
        form.fields['specialty'].choices = specialty_choices

    return render(request, 'appointments/create_appointment.html', {
        'form': form,
        'frequent': frequent,
        'others': others
    })

# Solo permite eliminar citas del usuario autenticado
@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)  # Verifica que la cita pertenezca al usuario

    if request.method == "POST":
        appointment.delete()
        return redirect('appointment_list')  # Redirige a la lista de citas después de eliminar

    return render(request, 'appointments/delete_appointment.html', {'appointment': appointment})
