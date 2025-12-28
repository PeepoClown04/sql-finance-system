import psycopg2
import os
from dotenv import load_dotenv

# 1. Cargar variables del archivo .env
load_dotenv()

# 2. Obtener credenciales (Si no existen, usa valores por defecto o falla)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "finance_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD") # La contraseña es crítica

def crear_vista_inteligente():
    try:
        if not DB_PASS:
            print("❌ ERROR: No se encontró DB_PASS en el archivo .env")
            return

        print("🔌 Conectando a PostgreSQL usando credenciales del .env...")
        
        # Conexión limpia
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()

        # SQL de la Vista
        query_vista = """
        CREATE OR REPLACE VIEW kpi_bitcoin AS
        SELECT 
            AVG(precio) as precio_promedio,
            MAX(precio) as precio_maximo,
            MIN(precio) as precio_minimo,
            COUNT(*) as total_registros,
            MAX(fecha) as ultima_actualizacion
        FROM bitcoin_history;
        """

        cur.execute(query_vista)
        conn.commit()
        
        print("✅ ÉXITO: Vista 'kpi_bitcoin' actualizada correctamente.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")

if __name__ == "__main__":
    crear_vista_inteligente()