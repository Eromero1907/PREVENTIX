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
    if not os.path.exists(MODEL_PATH):
        train_recommendation_model()

    knn = joblib.load(MODEL_PATH)

    appointments = (
        Appointment.objects
        .filter(user_id=user_id)
        .exclude(specialty__isnull=True)
        .exclude(specialty='')
        .values('specialty')
        .annotate(count=Count('id'), last_date=Max('date'))
    )

    df = pd.DataFrame(appointments)
    if df.empty:
        return pd.DataFrame()

    df['user_id'] = user_id
    df['last_date'] = pd.to_datetime(df['last_date'])
    df['timestamp'] = df['last_date'].apply(lambda x: x.timestamp())
    df['date'] = df['timestamp']
    df = df.dropna(subset=['count', 'date'])

    n_neighbors = min(3, len(df))
    distances, indices = knn.kneighbors(df[['user_id', 'count', 'date']], n_neighbors=n_neighbors)

    valid_indices = [i for i in indices[0] if i < len(df)]
    if not valid_indices:
        return pd.DataFrame()

    recommended = df.iloc[valid_indices].copy()
    recommended.loc[:, 'formatted_date'] = recommended['last_date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    return recommended[['specialty', 'formatted_date']]


