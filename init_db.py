import os
import psycopg2
from dotenv import load_dotenv

# 1. Cargar credenciales
load_dotenv()

try:
    # 2. Establecer conexión (El Puente)
    DATABASE_URL = os.getenv("DB_URL")
    conn = psycopg2.connect(DATABASE_URL)
    
    # 3. Crear el Cursor (El obrero que ejecuta las órdenes)
    cur = conn.cursor()
    
    print("✅ Conexión exitosa a PostgreSQL")

    # 4. Ejecutar SQL (Lenguaje de Base de Datos)
    # Creamos una tabla llamada 'bitcoin_history' si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bitcoin_history (
            id SERIAL PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            precio DECIMAL(10, 2),
            moneda VARCHAR(10)
        );
    """)
    
    # 5. Insertar un dato de prueba
    cur.execute("""
        INSERT INTO bitcoin_history (precio, moneda)
        VALUES (95000.50, 'BTC');
    """)
    
    # 6. COMMIT (Guardar cambios permanentemente)
    # Sin esto, los datos se pierden al cerrar la conexión.
    conn.commit()
    print("✅ Tabla creada y dato de prueba insertado")

    # 7. Cerrar conexión
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Error fatal: {e}")