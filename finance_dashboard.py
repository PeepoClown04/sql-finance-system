import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(page_title="Crypto Dashboard Pro", layout="wide", page_icon="💰")

# Cargar variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE CONEXIÓN ---
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'), # Asegúrate que este nombre coincida con tu DB
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')        # Tu contraseña
        )
        return conn
    except Exception as e:
        st.error(f"❌ Error conectando a la base de datos: {e}")
        return None

# --- NUEVA FUNCIÓN: CARGAR KPIs DESDE LA VISTA SQL ---
def cargar_kpis():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # AQUÍ ESTÁ LA MAGIA: Consultamos la VISTA, no la tabla cruda
        cur.execute("SELECT * FROM kpi_bitcoin")
        data = cur.fetchone() # Devuelve una sola fila con los promedios listos
        cur.close()
        conn.close()
        return data
    return None

# --- FUNCIÓN ORIGINAL: CARGAR DATOS PARA EL GRÁFICO ---
def cargar_datos_grafico():
    conn = get_db_connection()
    if conn:
        query = "SELECT fecha, precio FROM bitcoin_history ORDER BY fecha ASC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- INTERFAZ DEL DASHBOARD ---
st.title("💰 Monitor Financiero Inteligente")
st.markdown("Datos en tiempo real procesados por **PostgreSQL Views**.")

# 1. MOSTRAR KPIs (Métricas)
kpis = cargar_kpis()

if kpis:
    # kpis es una tupla: (promedio, max, min, count, ultima_fecha)
    precio_promedio = kpis[0]
    precio_maximo = kpis[1]
    precio_minimo = kpis[2]
    total_datos = kpis[3]
    
    # Crear 4 columnas para las tarjetas
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Precio Promedio", f"${precio_promedio:,.2f}")
    col2.metric("Máximo Histórico", f"${precio_maximo:,.2f}")
    col3.metric("Mínimo Histórico", f"${precio_minimo:,.2f}")
    col4.metric("Datos Analizados", f"{total_datos} registros")
    
    st.success(f"Última actualización de DB: {kpis[4]}")

else:
    st.warning("⚠️ No se pudieron cargar los KPIs. Revisa si la vista 'kpi_bitcoin' existe.")

st.markdown("---")

# 2. MOSTRAR GRÁFICO (Lo que ya tenías)
st.subheader("Tendencia de Mercado (BTC/USD)")
df = cargar_datos_grafico()

if not df.empty:
    fig = px.line(df, x='fecha', y='precio', title='Evolución de Precio')
    fig.update_layout(xaxis_title='Hora', yaxis_title='Precio USD', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Esperando datos en la base de datos...")

# Botón de recarga manual
if st.button('🔄 Actualizar Datos'):
    st.rerun()