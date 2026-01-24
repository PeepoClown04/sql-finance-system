from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
import pandas as pd
import os
import traceback

app = FastAPI(title="Bitcoin ML Predictor")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "bitcoin_predictor.joblib")

model = None
try:
    model = load(MODEL_PATH)
    print("✅ Modelo cargado en memoria.")
except:
    print("⚠️  Advertencia: No se encontró modelo .joblib. Ejecuta trainer.py primero.")


# DTO (Data Transfer Object) en Inglés para consistencia con el modelo
class MarketFeatures(BaseModel):
    volatility_3h: float
    trend_3h: float
    momentum: float
    current_price: float


@app.post("/predict")
def predict_price(features: MarketFeatures):
    if not model:
        raise HTTPException(status_code=503, detail="Modelo no entrenado")

    try:
        # Pydantic v2 syntax
        data = features.model_dump()
        input_df = pd.DataFrame([data])

        # Inferencia
        pred = model.predict(input_df)[0]

        return {
            "status": "success",
            "current_price": features.current_price,
            "predicted_price": pred
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))