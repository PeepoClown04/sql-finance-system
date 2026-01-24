import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_training_data():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL no encontrada en .env")

    engine = create_engine(db_url)

    # MAPPING CRÍTICO: Schema Español (DB) -> Schema Inglés (ML)
    # Filtramos por moneda si es necesario (asumimos que quieres entrenar con todo o solo USD)
    query = """
            SELECT fecha AS timestamp, 
        precio AS current_price
            FROM bitcoin_history
            ORDER BY fecha ASC; \
            """

    print(f"📡 Extrayendo datos de tabla 'bitcoin_history'...")
    df = pd.read_sql(query, engine)

    # Validación de datos mínimos
    if df.empty:
        raise ValueError("La tabla 'bitcoin_history' está vacía o no existe.")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    return df


if __name__ == "__main__":
    try:
        df = get_training_data()
        print(f"✅ Datos cargados: {len(df)} registros.")
        print(df.tail(3))
    except Exception as e:
        print(f"❌ Error: {e}")