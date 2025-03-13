from django.shortcuts import render, get_object_or_404, redirect
from .models import Prescription
from .forms import PrescriptionForm
from django.contrib import messages
from .models import MedicalFile
from .forms import MedicalFileForm
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required

@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.filter(user=request.user)  # Filtrar por usuario
    return render(request, 'medical_history/prescription_list.html', {'prescriptions': prescriptions})

@login_required
def create_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user  # Asignar el usuario actual
            prescription.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'medical_history/prescription_form.html', {'form': form})

@login_required
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, user=request.user)  # Asegurar que el usuario solo edite lo suyo
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'medical_history/prescription_form.html', {'form': form, 'prescription': prescription})

@login_required
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, user=request.user)  # Asegurar que solo pueda borrar lo suyo
    if request.method == "POST":
        prescription.delete()
        messages.success(request, "Prescripción eliminada correctamente.")
    return redirect('prescription_list')

@login_required
def medical_history(request):
    files = MedicalFile.objects.filter(user=request.user)  # Filtrar archivos del usuario
    formatted_files = [
        {
            'id': file.id,
            'title': file.title,
            'uploaded_at': localtime(file.uploaded_at).strftime("%d/%m/%Y %H:%M")
        } 
        for file in files
    ]
    return render(request, 'medical_history.html', {'files': formatted_files})

@login_required
def add_file(request):
    if request.method == 'POST':
        form = MedicalFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # Asignar el usuario actual
            file_instance.save()
            return redirect('medical_history')
    else:
        form = MedicalFileForm()
    return render(request, 'add_file.html', {'form': form})

@login_required
def edit_file(request, file_id):
    file_instance = get_object_or_404(MedicalFile, id=file_id, user=request.user)  # Asegurar que solo edite su archivo
    if request.method == 'POST':
        form = MedicalFileForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            form.save()
            return redirect('medical_history')
    else:
        form = MedicalFileForm(instance=file_instance)
    return render(request, 'edit_file.html', {'form': form, 'file_instance': file_instance})

@login_required
def delete_file(request, file_id):
    file_instance = get_object_or_404(MedicalFile, id=file_id, user=request.user)  # Asegurar que solo pueda borrar lo suyo
    if request.method == 'POST':
        file_instance.delete()
        return redirect('medical_history')
    return render(request, 'delete_file.html', {'file_instance': file_instance})

@login_required
def view_file(request, file_id):
    file = get_object_or_404(MedicalFile, id=file_id, user=request.user)  # Restringir acceso a solo sus archivos
    return render(request, 'view_file.html', {'file': file})