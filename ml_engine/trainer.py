import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from joblib import dump
from ml_engine.data_loader import get_training_data
import os

# Ruta absoluta para evitar errores de "file not found" en ejecución cruzada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "bitcoin_predictor.joblib")


def make_features(df):
    df = df.copy()
    # Feature Engineering (Vectorizado)
    df['log_ret'] = np.log(df['current_price'] / df['current_price'].shift(1))
    df['volatility_3h'] = df['log_ret'].rolling(window=3).std()
    df['trend_3h'] = df['current_price'].rolling(window=3).mean()
    df['momentum'] = df['current_price'].diff()
    df['target_next_price'] = df['current_price'].shift(-1)
    return df.dropna()


def train_model():
    print("🚀 Iniciando pipeline de entrenamiento...")
    try:
        raw_df = get_training_data()
    except Exception as e:
        print(f"Error de carga: {e}")
        return

    if len(raw_df) < 5:
        print("⚠️  DATA INSUFICIENTE: Se necesitan mínimo 5 registros para generar features.")
        return

    processed_df = make_features(raw_df)

    # Features usadas para inferencia
    features = ['volatility_3h', 'trend_3h', 'momentum', 'current_price']
    X = processed_df[features]
    y = processed_df['target_next_price']

    # Entrenamiento (Full dataset si es pequeño, para maximizar aprendizaje reciente)
    model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X, y)

    dump(model, MODEL_PATH)
    print(f"✅ Modelo entrenado y guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()