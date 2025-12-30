import time
import requests
import psycopg2
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DB_URL"))
        return conn
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

def fetch_price():
    # Usamos Bitcoin IDs hardcodeados para estabilidad
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        print(f"⚠️ Error API CoinGecko: {e}")
        return None

def main():
    print("🚀 Iniciando Ingestor de Datos (ETL) v2.0...")
    
    # 1. Asegurar que la tabla existe (Self-Healing)
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Creamos la tabla simple. Si ya existe con columna 'moneda', PostgreSQL lo manejará.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bitcoin_history (
                    id SERIAL PRIMARY KEY,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    precio DECIMAL(10, 2),
                    moneda VARCHAR(10) DEFAULT 'BTC'
                );
            """)
            conn.commit()
            print("✅ Verificación de integridad de tabla: OK")
            conn.close()
        except Exception as e:
            print(f"⚠️ Advertencia SQL (Tabla): {e}")

    # 2. Bucle Infinito de Ingesta
    while True:
        price = fetch_price()
        if price:
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insertamos precio. Si la tabla vieja pide 'moneda', usamos el default o null.
                    # Para máxima compatibilidad con tu tabla vieja, inyectamos 'BTC' explícitamente.
                    cursor.execute("INSERT INTO bitcoin_history (precio, moneda) VALUES (%s, 'BTC')", (price,))
                    conn.commit()
                    print(f"💾 Dato guardado: ${price} USD")
                    cursor.close()
                    conn.close()
                except Exception as e:
                    # Si falla por columna 'moneda' inexistente, intentamos insert simple
                    try:
                        conn.rollback()
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO bitcoin_history (precio) VALUES (%s)", (price,))
                        conn.commit()
                        print(f"💾 Dato guardado (Schema V2): ${price} USD")
                    except Exception as e2:
                        print(f"❌ Error SQL Fatal: {e2}")
        
        # Flush para que los logs salgan inmediatos en Docker
        sys.stdout.flush() 
        time.sleep(60)

if __name__ == "__main__":
    main()