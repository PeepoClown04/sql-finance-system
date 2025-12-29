# Usamos una imagen base oficial de Python ligera
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y fuerza salida en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar (gcc, libpq)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero los requirements (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalamos librerías Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código del proyecto
COPY . .

# Exponemos el puerto de Streamlit
EXPOSE 8501

# Comando de arranque por defecto (Esto se sobrescribe en el docker-compose)
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]