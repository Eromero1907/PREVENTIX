from django.urls import path
from .views import medical_history, add_file, edit_file, delete_file, view_file
from .views import prescription_list, create_prescription, edit_prescription, delete_prescription

urlpatterns = [
    path('prescriptions/', prescription_list, name='prescription_list'),
    path('prescriptions/create/', create_prescription, name='create_prescription'),
    path('prescriptions/<int:pk>/edit/', edit_prescription, name='edit_prescription'),
    path('prescriptions/<int:pk>/delete/', delete_prescription, name='delete_prescription'),
    path('', medical_history, name='medical_history'),
    path('add/', add_file, name='add_file'),
    path('edit/<int:file_id>/', edit_file, name='edit_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('view/<int:file_id>/', view_file, name='view_file'),
]
