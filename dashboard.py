import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Configuración de la página
st.set_page_config(page_title="Crypto Monitor", page_icon="📈")
load_dotenv()

# 2. Título
st.title("💸 Bitcoin Price Tracker")
st.write("Datos en tiempo real desde Neon DB (Ingestado por Azure Bot)")

# 3. Función para conectar a la DB
def get_data():
    conn = psycopg2.connect(os.getenv("DB_URL"))
    # CORREGIDO: Usamos 'fecha' en lugar de 'timestamp'
    query = "SELECT * FROM bitcoin_history ORDER BY fecha DESC LIMIT 500"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 4. Mostrar Datos
try:
    df = get_data()

    # CORREGIDO: Usamos la columna 'precio'
    latest_price = df.iloc[0]['precio']
    st.metric(label="Precio Actual (USD)", value=f"${latest_price:,.2f}")

    # Gráfico
    st.subheader("Tendencia de Precio")

    # CORREGIDO: Usamos 'fecha' como índice y graficamos 'precio'
    chart_data = df.set_index('fecha')
    st.line_chart(chart_data['precio'])

    # Tabla de datos brutos
    if st.checkbox("Ver datos crudos"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Error conectando a la base de datos: {e}")