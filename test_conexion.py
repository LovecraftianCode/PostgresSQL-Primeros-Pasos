from config import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT version();"))
        print("Conexión exitosa")
        print(resultado.fetchone())
except Exception as e:
    print(f"Error: {e}")