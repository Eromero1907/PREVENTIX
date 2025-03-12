from django.urls import path
from .views import prescription_list, create_prescription, edit_prescription, delete_prescription

urlpatterns = [
    path('prescriptions/', prescription_list, name='prescription_list'),
    path('prescriptions/create/', create_prescription, name='create_prescription'),
    path('prescriptions/<int:pk>/edit/', edit_prescription, name='edit_prescription'),
    path('prescriptions/<int:pk>/delete/', delete_prescription, name='delete_prescription'),
]
