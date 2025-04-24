from django.db.models import Count, Max
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
from .models import Appointment
import os
from django.utils import timezone

MODEL_PATH = 'appointments/models/knn_model.pkl'

# Función para entrenar y guardar el modelo
def train_recommendation_model():
    # Agregar la cuenta de citas por usuario y especialidad
    appointments = (
        Appointment.objects
        .exclude(specialty__isnull=True)
        .exclude(specialty='')
        .values('user_id', 'specialty')
        .annotate(count=Count('id'), last_date=Max('date'))
    )

    # Convertir a DataFrame
    data = pd.DataFrame(appointments)
    if data.empty:
        print("No hay datos suficientes para entrenar el modelo.")
        return

    # Procesar campos
    data['last_date'] = pd.to_datetime(data['last_date'])
    data['date'] = data['last_date'].map(lambda x: x.timestamp())
    X = data[['user_id', 'count', 'date']]

    # Entrenar y guardar el modelo
    knn = NearestNeighbors(n_neighbors=3)
    knn.fit(X)
    joblib.dump(knn, MODEL_PATH)
    print("Modelo KNN entrenado y guardado correctamente.")

# Función para recomendar citas
def recommend_appointments(user_id):
    # Verificar que el modelo existe
    if not os.path.exists(MODEL_PATH):
        print("Modelo no encontrado. Entrenando uno nuevo...")
        train_recommendation_model()

    # Cargar modelo
    knn = joblib.load(MODEL_PATH)

    # Agregar la cuenta de citas por especialidad del usuario
    appointments = (
        Appointment.objects
        .filter(user_id=user_id)
        .exclude(specialty__isnull=True)
        .exclude(specialty='')
        .values('specialty')
        .annotate(count=Count('id'), last_date=Max('date'))
    )

    # Convertir a DataFrame
    df = pd.DataFrame(appointments)
    if df.empty:
        return pd.DataFrame()  # No hay recomendaciones si no hay citas

    df['user_id'] = user_id
    df['last_date'] = pd.to_datetime(df['last_date'])  # Asegurarse de que last_date es datetime

    # Convertir 'last_date' a timestamp (numérico)
    df['timestamp'] = df['last_date'].apply(lambda x: x.timestamp())  # Convertir a timestamp (segundos desde 1970)

    # Usar 'timestamp' como una característica numérica para las recomendaciones
    df['date'] = df['timestamp']  # Usamos 'timestamp' como número

    # Asegurarse de no tener NaNs
    df = df.dropna(subset=['count', 'date'])

    # Recomendación
    distances, indices = knn.kneighbors(df[['user_id', 'count', 'date']])
    recommended = df.iloc[indices[0]]

    # Devolver las citas recomendadas con solo la fecha
    recommended['formatted_date'] = recommended['last_date'].apply(lambda x: x.strftime('%Y-%m-%d'))  # Solo la fecha

    return recommended[['specialty', 'formatted_date']]

