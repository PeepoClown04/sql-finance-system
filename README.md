# ⚡ Bitcoin Algorithmic Tracker + AI (MLOps Edition)

Plataforma de ingeniería de datos financiera y predicción algorítmica. Ingesta datos de criptomonedas, almacena en Data Warehouse (Cloud), y utiliza un **microservicio de Inteligencia Artificial** para predecir precios futuros en tiempo real.

[![Deployment](https://img.shields.io/badge/Azure-Docker_Container-blue?logo=microsoftazure)](https://azure.microsoft.com)
[![Architecture](https://img.shields.io/badge/Microservices-Docker_Compose-2496ED?logo=docker)](https://www.docker.com/)
[![AI Model](https://img.shields.io/badge/ML-Scikit_Learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Neon-Serverless_Postgres-green?logo=postgresql)](https://neon.tech)
[![Frontend](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io)

### 🔗 Demo en Vivo: [https://finance.dev-peepo.me](https://finance.dev-peepo.me/)

---

## 🏗 Arquitectura de Microservicios (Docker)

El sistema opera bajo una arquitectura orquestada por **Docker Compose** con 3 contenedores aislados:

1.  **🧠 ML Brain (API de Inferencia):**
    * Microservicio expuesto con **FastAPI**.
    * Ejecuta un modelo **RandomForestRegressor** entrenado para predecir precios ($t+1$) basándose en tendencia, volatilidad y momentum.
    * Arquitectura "Serverless-ready".

2.  **📊 Dashboard (Frontend):**
    * Interfaz en **Streamlit** conectada a la red interna de Docker.
    * Consume datos históricos de NeonDB y solicita predicciones en tiempo real a la API de ML.
    * Cálculo de indicadores técnicos en vivo (SMA 50, Log Returns).

3.  **🤖 ETL Bot (Ingesta):**
    * Worker autónomo en Python.
    * Programado vía **Cronjob** en el host para ejecución horaria.
    * Extrae datos de CoinGecko, normaliza y persiste en **Neon PostgreSQL**.

---

## 🔮 Capacidades de IA (Neural Forecasting)

El sistema incluye un pipeline de Machine Learning completo:
* **Feature Engineering:** Generación de ventanas móviles (Rolling Windows) para volatilidad y tendencia.
* **Modelo:** Random Forest Regressor (Scikit-Learn).
* **Métrica:** Entrenado para minimizar el MAE (Error Absoluto Medio).
* **Inferencia:** Predicción de precio de cierre para la próxima hora.

---

## 🛠 Tech Stack

* **Infraestructura:** Microsoft Azure VM, Docker, Docker Compose, Nginx.
* **MLOps:** FastAPI, Uvicorn, Scikit-Learn, Joblib.
* **Data Engineering:** Python 3.10, Pandas, SQLAlchemy, Neon DB (Postgres).
* **Visualización:** Streamlit.

---

## ⚙️ Instalación Local (Dockerizada)

Olvídate de configurar entornos virtuales manuales. El proyecto es "Plug & Play" con Docker.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/PeepoClown04/sql-finance-system.git](https://github.com/PeepoClown04/sql-finance-system.git)
    cd sql-finance-system
    ```

2.  **Configurar Variables:**
    Crea un archivo `.env` en la raíz con tus credenciales:
    ```ini
    DATABASE_URL="postgresql://usuario:password@endpoint.neon.tech/finance_db?sslmode=require"
    API_URL="http://ml-brain:8000"  # Comunicación interna de Docker
    ```

3.  **Desplegar Arquitectura:**
    ```bash
    docker-compose up --build
    ```
    * Dashboard: `http://localhost:8501`
    * API ML: `http://localhost:8000/docs`

---

## 🚀 Operación en Producción (Azure)

El sistema corre en segundo plano (`detached`) y el bot se gestiona automáticamente.

**Comandos de Gestión:**

```bash
# 1. Ver estado de los contenedores (Cerebro + Frontend)
docker ps

# 2. Ver logs de predicción de la IA
docker logs -f crypto_ml_api

# 3. Ejecutar el Bot de Ingesta manualmente (fuera de horario)
docker start finance-etl

# 4. Actualizar código y reconstruir sin downtime prolongado
git pull origin main
docker-compose up --build -d
