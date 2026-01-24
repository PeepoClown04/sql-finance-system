import streamlit as st
import psycopg2
import pandas as pd
import os
import requests
import numpy as np
from dotenv import load_dotenv
from etl_job import get_db_connection

# 1. Configuración y Estilos
st.set_page_config(page_title="Crypto Monitor Pro", page_icon="📊", layout="wide")
load_dotenv()

# URL dinámica: Detecta si corre en Docker (ml-brain) o Local (localhost)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)


# 2. Funciones Auxiliares
@st.cache_data(ttl=60)
def get_data():
    conn = get_db_connection()
    # Traemos datos, pero OJO: Pandas necesita orden ascendente para calcular medias móviles correctamente
    query = "SELECT * FROM bitcoin_history ORDER BY fecha DESC LIMIT 2000"
    df = pd.read_sql(query, conn)
    conn.close()
    # Invertimos para tener cronología correcta (Viejo -> Nuevo)
    return df.sort_values(by='fecha', ascending=True).reset_index(drop=True)


def get_prediction(price, trend, volatility, momentum):
    """Consulta al microservicio de IA"""
    try:
        payload = {
            "current_price": price,
            "trend_3h": trend,
            "volatility_3h": volatility,
            "momentum": momentum
        }
        # Timeout corto para no congelar el dashboard
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=2)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error API: {e}")
        return None


# 3. Renderizado Principal
try:
    st.title("⚡ Bitcoin Algorithmic Tracker")
    st.markdown("---")

    df = get_data()

    if not df.empty and len(df) > 50:
        # --- CÁLCULO DE INDICADORES (Feature Engineering) ---

        # 1. Indicadores Visuales (SMA 50)
        df['SMA_50'] = df['precio'].rolling(window=50).mean()

        # 2. Indicadores para IA (Deben ser idénticos al entrenamiento)
        # Log Returns para volatilidad estable
        df['log_ret'] = np.log(df['precio'] / df['precio'].shift(1))

        # Features exactos del modelo
        last_row = df.iloc[-1]

        # Calculamos sobre la serie completa y tomamos el último valor
        series_trend_3h = df['precio'].rolling(window=3).mean()
        series_vol_3h = df['log_ret'].rolling(window=3).std()
        series_mom = df['precio'].diff()

        # Valores actuales para enviar a la API
        current_price = float(last_row['precio'])
        feat_trend = float(series_trend_3h.iloc[-1])
        feat_vol = float(series_vol_3h.iloc[-1])
        feat_mom = float(series_mom.iloc[-1])

        # --- SECCIÓN DE PREDICCIÓN (NUEVO) ---
        st.subheader("🔮 Neural Forecasting (RandomForest)")

        prediction_data = get_prediction(current_price, feat_trend, feat_vol, feat_mom)

        cols_pred = st.columns(3)

        with cols_pred[0]:
            st.metric("Precio Actual", f"${current_price:,.2f}")

        with cols_pred[1]:
            if prediction_data:
                pred_price = prediction_data.get("predicted_price", 0)
                delta = pred_price - current_price
                st.metric(
                    label="Predicción (Próxima Hora)",
                    value=f"${pred_price:,.2f}",
                    delta=f"{delta:,.2f} USD"
                )
            else:
                st.warning("⚠️ Módulo de IA desconectado")

        with cols_pred[2]:
            st.caption(
                f"Inputs del Modelo:\n- Tendencia (3h): {feat_trend:.2f}\n- Volatilidad: {feat_vol:.4f}\n- Momentum: {feat_mom:.2f}")

        st.divider()

        # --- KPIs CLÁSICOS ---
        prev_price = df.iloc[-2]['precio']
        pct_change = ((current_price - prev_price) / prev_price) * 100
        volatility_display = df['precio'].rolling(window=20).std().iloc[-1]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Variación (1h)", f"{pct_change:.2f}%", delta=pct_change)
        with col2:
            st.metric("Volatilidad Histórica (20p)", f"${volatility_display:,.2f}")
        with col3:
            st.metric("Máximo (24h)", f"${df['precio'].tail(24).max():,.2f}")
        with col4:
            st.metric("Mínimo (24h)", f"${df['precio'].tail(24).min():,.2f}")

        # --- GRÁFICOS ---
        st.markdown("### 📈 Análisis Técnico")
        chart_data = df[['fecha', 'precio', 'SMA_50']].set_index('fecha')
        st.line_chart(chart_data, color=["#00FF00", "#0088FF"])

    else:
        st.warning("Recopilando datos... Se necesitan al menos 50 registros para inicializar indicadores.")

except Exception as e:
    st.error(f"Error crítico en Dashboard: {e}")