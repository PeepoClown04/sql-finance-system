# Dockerfile.ml
FROM python:3.10-slim

WORKDIR /app

# Instalamos dependencias para compilar
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiamos solo lo necesario para la API
COPY requirements_ml.txt .
RUN pip install --no-cache-dir -r requirements_ml.txt

# Copiamos todo el código
COPY . .

# Exponemos el puerto de la API (no el de Streamlit)
EXPOSE 8000

# Comando para levantar el servidor FastAPI
CMD ["uvicorn", "ml_engine.api:app", "--host", "0.0.0.0", "--port", "8000"]