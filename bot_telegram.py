import time
import requests
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar configuraciones
load_dotenv()

# Configuración de Alertas
PRECIO_OBJETIVO = 97000.00 # Cambia esto al precio que quieras vigilar
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_bitcoin_price():
    """Consulta la API de CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        print(f"⚠️ Error API: {e}")
        return None

def save_to_db(price):
    """Guarda el precio en PostgreSQL"""
    try:
        conn = psycopg2.connect(os.getenv("DB_URL"))
        cur = conn.cursor()
        query = "INSERT INTO bitcoin_history (precio, moneda) VALUES (%s, %s)"
        cur.execute(query, (price, 'BTC'))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Guardado: ${price:,.2f} USD")
    except Exception as e:
        print(f"❌ Error DB: {e}")

def send_alert(price):
    """Envía alerta a Telegram si supera el objetivo"""
    try:
        mensaje = f"🚀 <b>ALERTA BITCOIN</b>\n\nEl precio superó los <b>${PRECIO_OBJETIVO:,.2f}</b>\nActual: <b>${price:,.2f} USD</b>"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
        requests.post(url, data=data)
        print("📨 Alerta enviada a Telegram")
    except Exception as e:
        print(f"❌ Error Telegram: {e}")

# --- BUCLE PRINCIPAL ---
print(f"🤖 Monitor Iniciado. Alerta configurada en: ${PRECIO_OBJETIVO:,.2f}")

while True:
    precio = get_bitcoin_price()
    
    if precio:
        # 1. Guardar
        save_to_db(precio)
        
        # 2. Verificar Alerta
        if precio > PRECIO_OBJETIVO:
            send_alert(precio)
            # Subimos el objetivo para no spamear (o podrías poner un sleep largo)
            PRECIO_OBJETIVO += 500 
            print(f"📈 Nuevo objetivo fijado en: ${PRECIO_OBJETIVO:,.2f}")
    
    time.sleep(60) # Esperar 1 minuto