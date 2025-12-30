import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Configuración y Estilos
st.set_page_config(page_title="Crypto Monitor Pro", page_icon="📊", layout="wide")
load_dotenv()

# Estilos CSS personalizados para "dark mode" agresivo
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

# 2. Conexión a Base de Datos
@st.cache_data(ttl=60)
def get_data():
    conn = psycopg2.connect(os.getenv("DB_URL"))
    # Traemos más datos para poder calcular tendencias
    query = "SELECT * FROM bitcoin_history ORDER BY timestamp DESC LIMIT 2000;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. Renderizado
try:
    st.title("⚡ Bitcoin Algorithmic Tracker")
    st.markdown("---")
    
    df = get_data()
    
    if not df.empty:
        # --- CÁLCULO DE INDICADORES ---
        current_price = df.iloc[-1]['precio']
        prev_price = df.iloc[-2]['precio']
        price_change = current_price - prev_price
        pct_change = (price_change / prev_price) * 100
        
        # Media Móvil Simple (SMA) de 50 periodos (aprox 50 minutos si es por minuto)
        df['SMA_50'] = df['precio'].rolling(window=50).mean()
        
        # Volatilidad (Desviación Estándar de 20 periodos)
        volatility = df['precio'].rolling(window=20).std().iloc[-1]

        # --- KPIs SUPERIORES ---
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Precio Actual", f"${current_price:,.2f}", f"{pct_change:.2f}%")
        with col2:
            st.metric("Volatilidad (20p)", f"${volatility:,.2f}")
        with col3:
            max_price = df['precio'].max()
            st.metric("Máximo Reciente", f"${max_price:,.2f}")
        with col4:
            min_price = df['precio'].min()
            st.metric("Mínimo Reciente", f"${min_price:,.2f}")

        # --- GRÁFICOS AVANZADOS ---
        st.markdown("### 📈 Tendencia vs Media Móvil (SMA 50)")
        
        # Preparamos datos para el gráfico lineal
        chart_data = df[['fecha', 'precio', 'SMA_50']].set_index('fecha')
        
        # Gráfico de líneas con Streamlit nativo (rápido y limpio)
        st.line_chart(chart_data, color=["#00FF00", "#0088FF"])
        
        st.caption("La línea azul representa el suavizado del precio (SMA). Cruces pueden indicar señales de compra/venta.")

    else:
        st.warning("Esperando más datos para calcular indicadores...")

except Exception as e:
    st.error(f"Error del sistema: {e}")