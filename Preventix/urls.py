"""
URL configuration for Preventix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from preventixapp import views as preventixappViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', preventixappViews.home),
    path('register/', preventixappViews.register, name='register'),
    path('login/', preventixappViews.login_view, name='login'),
    path('dashboard/', preventixappViews.dashboard, name='dashboard'),
    path('dashboard/appointments/', preventixappViews.create_appointment, name='create_appointment'),
    path('appointments/delete/<int:appointment_id>/', preventixappViews.delete_appointment, name='delete_appointment'),
]
