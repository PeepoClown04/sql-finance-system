# SQL Finance Monitor & Alert System 📉

Sistema automatizado **ETL (Extract, Transform, Load)** que captura precios de criptomonedas en tiempo real, los almacena en una base de datos relacional y ofrece análisis inteligente mediante un Dashboard y Alertas Móviles.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)

## 🏗 Arquitectura

1.  **Motor de Ingesta:** Un bot en Python consulta la API de **CoinGecko** cada 60 segundos.
2.  **Capa de Almacenamiento:** Los datos crudos se persisten en **PostgreSQL**.
3.  **Capa de Inteligencia:** **Vistas SQL (Views)** calculan automáticamente los KPIs (Promedio, Máximo, Mínimo) para optimizar el rendimiento.
4.  **Visualización:** Un **Dashboard en Streamlit** lee directamente de las Vistas SQL.
5.  **Sistema de Notificación:** Alertas automáticas vía **Telegram** cuando se detectan anomalías de precio.

## ⚙️ Requisitos Previos

* Python 3.x
* PostgreSQL instalado y ejecutándose localmente.
* Un Token de Bot de Telegram (para las alertas).

## 🚀 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/PeepoClown04/sql-finance-system.git](https://github.com/PeepoClown04/sql-finance-system.git)
    cd sql-finance-system
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuración de Base de Datos:**
    * Crea una base de datos llamada `finance_db` en PostgreSQL.
    * Crea un archivo `.env` en la raíz con tus credenciales:
        ```ini
        DB_HOST=localhost
        DB_NAME=finance_db
        DB_USER=postgres
        DB_PASS=tu_password
        TELEGRAM_TOKEN=tu_token_telegram
        CHAT_ID=tu_chat_id
        ```

4.  **Inicializar el Sistema:**
    ```bash
    # Crea la tabla de precios
    python init_db.py
    
    # Crea la Capa de Inteligencia (Vistas SQL)
    python create_view.py
    ```

## 🖥️ Uso

### 1. Iniciar el Monitor & Bot
Este script corre en segundo plano, guardando datos y vigilando alertas.
```bash
python bot_telegram.py