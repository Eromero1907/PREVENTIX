from django.db.models import Count, Max
from datetime import date, timedelta
from appointments.models import Appointment

def get_user_appointment_stats(user):
    stats = (Appointment.objects
             .filter(user=user)
             .values('specialty')
             .annotate(total=Count('id'), last_date=Max('date'))
             .order_by('-total'))
    return stats

def get_forgotten_specialties(user, months_threshold=6):
    stats = get_user_appointment_stats(user)
    forgotten = []

    for item in stats:
        if item['last_date'] < (date.today() - timedelta(days=30 * months_threshold)):
            forgotten.append({
                'specialty': item['specialty'],
                'last_date': item['last_date'],
                'times_requested': item['total'],
                'reason': f"No solicitas esta especialidad desde hace más de {months_threshold} meses."
            })

    return forgotten
