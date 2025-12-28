# SQL Finance Logger 📉
![Status](https://img.shields.io/badge/Database-PostgreSQL-blue) ![Python](https://img.shields.io/badge/Python-3.x-yellow)

Sistema automatizado ETL (Extract, Transform, Load) que captura precios de criptomonedas en tiempo real y los almacena en una base de datos relacional para su análisis histórico.

## Arquitectura
1.  **Extractor:** Consulta la API de CoinGecko cada 10 segundos.
2.  **Loader:** Persiste los datos en PostgreSQL usando `psycopg2`.
3.  **Analytics:** Genera reportes estadísticos (Min, Max, Promedio) mediante consultas SQL.

## Requisitos Previos
- Python 3.x
- PostgreSQL instalado y corriendo localmente.

## Configuración

1.  Clonar el repositorio.
2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crear una base de datos en PostgreSQL llamada `finance_db`.
4.  Crear un archivo `.env` en la raíz con tus credenciales locales:
    ```ini
    DB_HOST=localhost
    DB_NAME=finance_db
    DB_USER=postgres
    DB_PASS=tu_password
    ```

## Uso

1.  **Inicializar la Tabla:**
    ```bash
    python init_db.py
    ```
2.  **Iniciar el Logger (Captura de datos):**
    ```bash
    python logger.py
    ```
3.  **Generar Reporte de Análisis:**
    ```bash
    python analytics.py
    ```
4.  **Iniciar Dashboard Visual:**
    Mantén el logger corriendo en una terminal y en otra ejecuta:
    ```bash
    streamlit run dashboard.py
    ```
    Accede a `http://localhost:8501` para ver el gráfico en tiempo real.