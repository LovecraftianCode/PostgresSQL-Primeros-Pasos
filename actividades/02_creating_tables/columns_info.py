import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import engine
from sqlalchemy import text

sql = text("""
    SELECT COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION
    FROM information_schema.columns
    WHERE table_name = :tabla
""")

with engine.connect() as conn:
    resultado = conn.execute(sql, {"tabla": "products"})
    for fila in resultado:
        print(fila)