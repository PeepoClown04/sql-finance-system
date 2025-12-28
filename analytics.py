import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def generar_reporte():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        
        # --- PREGUNTA 1: Estadísticas Básicas ---
        # Usamos funciones de agregación de SQL (MIN, MAX, AVG, COUNT)
        cur.execute("""
            SELECT 
                COUNT(*),
                MIN(precio),
                MAX(precio),
                AVG(precio)
            FROM bitcoin_history;
        """)
        
        # Obtenemos el resultado (una sola fila con 4 valores)
        datos = cur.fetchone()
        cantidad, minimo, maximo, promedio = datos
        
        print(f"📊 REPORTE DE MERCADO (Histórico)")
        print(f"--------------------------------")
        print(f"📡 Muestras tomadas: {cantidad}")
        print(f"🔻 Precio Mínimo:    ${minimo:,.2f}")
        print(f"🔺 Precio Máximo:    ${maximo:,.2f}")
        print(f"⚖️ Precio Promedio:  ${promedio:,.2f}")
        print(f"--------------------------------")

        # --- PREGUNTA 2: Último registro ---
        cur.execute("SELECT precio, fecha FROM bitcoin_history ORDER BY fecha DESC LIMIT 1;")
        ultimo_precio, ultima_fecha = cur.fetchone()
        
        print(f"🕒 Última actualización: {ultima_fecha} (${ultimo_precio:,.2f})")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error al analizar: {e}")

if __name__ == "__main__":
    generar_reporte()