from django.db import models
from django.conf import settings

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ahora usa settings.AUTH_USER_MODEL
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    specialty = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"
