from django.core.management.base import BaseCommand
from appointments.ml_model import train_recommendation_model

class Command(BaseCommand):
    help = 'Entrena el modelo de recomendación'

    def handle(self, *args, **kwargs):
        self.stdout.write('Entrenando el modelo de recomendación...')
        train_recommendation_model()
        self.stdout.write('Modelo entrenado y guardado correctamente.')
