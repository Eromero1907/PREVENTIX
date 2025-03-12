from django.shortcuts import render, get_object_or_404, redirect
from .models import Prescription
from .forms import PrescriptionForm
from django.contrib import messages

def prescription_list(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'medical_history/prescription_list.html', {'prescriptions': prescriptions})

def create_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'medical_history/prescription_form.html', {'form': form})

def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'medical_history/prescription_form.html', {'form': form, 'prescription': prescription})

def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    
    if request.method == "POST":
        prescription.delete()
        messages.success(request, "Prescripción eliminada correctamente.")
        return redirect('prescription_list')  # Asegúrate de que esta es la vista correcta

    return redirect('prescription_list')