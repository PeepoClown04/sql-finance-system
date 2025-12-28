import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.express as px
from dotenv import load_dotenv

# Configuración de página
st.set_page_config(page_title="Crypto Monitor SQL", layout="wide")
load_dotenv()

# --- CONEXIÓN A BASE DE DATOS ---
def load_data():
    """Conecta a Postgres y descarga todo el historial"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        # Pandas puede leer SQL directamente y convertirlo en DataFrame
        query = "SELECT * FROM bitcoin_history ORDER BY fecha ASC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- INTERFAZ GRÁFICA ---
st.title("📡 Monitor de Precios en Tiempo Real")
st.markdown("Este dashboard lee datos directamente de **PostgreSQL**.")

# Botón manual de recarga (Streamlit no se recarga solo por defecto para ahorrar recursos)
if st.button("🔄 Actualizar Datos"):
    st.rerun()

# Cargar datos
df = load_data()

if not df.empty:
    # --- METRICAS PRINCIPALES (KPIs) ---
    ultimo_registro = df.iloc[-1]
    precio_actual = ultimo_registro['precio']
    hora_actual = ultimo_registro['fecha']
    
    # Calculamos variación respecto al registro anterior (si existe)
    delta = 0
    if len(df) > 1:
        anterior = df.iloc[-2]['precio']
        delta = precio_actual - anterior

    col1, col2, col3 = st.columns(3)
    col1.metric("Precio Actual (BTC)", f"${precio_actual:,.2f}", f"{delta:,.2f}")
    col2.metric("Última Actualización", f"{hora_actual}")
    col3.metric("Total Registros en DB", len(df))

    st.markdown("---")

    # --- GRÁFICO DE LÍNEA ---
    st.subheader("Tendencia de Mercado")
    fig = px.line(df, x='fecha', y='precio', title='Evolución del Precio (BTC/USD)', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # --- TABLA DE DATOS RECIENTES ---
    with st.expander("Ver últimos 10 registros crudos"):
        st.dataframe(df.tail(10).sort_values(by="fecha", ascending=False))

else:
    st.warning("⚠️ La base de datos está vacía. Ejecuta 'logger.py' para generar datos.")