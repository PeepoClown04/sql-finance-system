import requests
import psycopg2
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DB_URL"))
        return conn
    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return None


def fetch_price():
    # IDs hardcodeados para estabilidad
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        print(f"Error API CoinGecko: {e}")
        return None


def main():
    print("Iniciando ejecucion programada...")

    # Verificacion de integridad de tabla (Self-Healing)
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS bitcoin_history
                           (
                               id
                               SERIAL
                               PRIMARY
                               KEY,
                               fecha
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               precio
                               DECIMAL
                           (
                               10,
                               2
                           ),
                               moneda VARCHAR
                           (
                               10
                           ) DEFAULT 'BTC'
                               );
                           """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Advertencia SQL (Tabla): {e}")

    # Ejecucion unica
    price = fetch_price()

    if price:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Intento principal con columna moneda
                cursor.execute("INSERT INTO bitcoin_history (precio, moneda) VALUES (%s, 'BTC')", (price,))
                conn.commit()
                print(f"Dato guardado: ${price} USD")
                cursor.close()
                conn.close()
            except Exception:
                # Fallback para compatibilidad con esquema antiguo
                try:
                    conn.rollback()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO bitcoin_history (precio) VALUES (%s)", (price,))
                    conn.commit()
                    print(f"Dato guardado (Schema V1): ${price} USD")
                except Exception as e2:
                    print(f"Error SQL Fatal: {e2}")
    else:
        print("No se pudo obtener el precio.")

    print("Finalizado.")
    sys.stdout.flush()


if __name__ == "__main__":
    main()