# Conexión a PostgreSQL con Python

Práctica personal de conexión a una base de datos PostgreSQL desde Python usando SQLAlchemy, psql y psycopg2.

## Entorno

- **Sistema operativo:** Arch Linux
- **Shell:** Bash (`/usr/bin/bash`)
- **Base de datos:** PostgreSQL
- **Cliente gráfico:** DBeaver
- **Editor:** Visual Studio Code

## Dependencias

### Instalación de paquetes del sistema (pacman)

```bash
sudo pacman -S postgresql python-psycopg2 python-dotenv python-sqlalchemy
```
## Estructura del proyecto

```
02 Conexion_a_BDD_py/
├── .env.example          # Plantilla de credenciales
├── .gitignore            # Archivos excluidos del control de versiones
├── config.py             # Carga el .env y crea el engine de SQLAlchemy
├── test_conexion.py      # Script de prueba de conexión
├── README.md
└── actividades/
    └── 02_creating_tables/
        ├── actividad.sql       # Consulta SQL del libro
        └── columns_info.py     # Script Python que ejecuta la consulta
```

## Carga de la base de datos de ejemplo (SQL for Data Analytics)

### Descargar la BDD de 
https://github.com/PacktPublishing/SQL-for-Data-Analytics-Fourth-Edition/tree/main/Datasets
   
   -Se ocupara el achivo data.dump

### Conectarse a la base de datos de mantenimiento y creacion de la BDD:
   ```bash
   psql -U craftiancode -d postgres

    #Crear la base de datos del libro
    CREATE DATABASE sqlda;

    #Conectarse a la nueva base
    \i /ruta/al/data.dump
```

<img width="937" height="492" alt="creacion-y-carga-de-la-bdd" src="https://github.com/user-attachments/assets/1f0a65dd-142d-40ba-88f6-1a973ea3542e" />

### Verificar la carga:

   ```bash
SELECT * FROM public.products LIMIT 5;
```

<img width="1890" height="564" alt="2026-09-24-001318_hyprshot" src="https://github.com/user-attachments/assets/da33dfdb-8486-43ad-991e-37e108451d98" />

## Variables de entorno

El archivo `.env` contiene las credenciales reales y **nunca debe subirse al repositorio**. El archivo `.env.example` es la plantilla que sí se sube:

<img width="1920" height="1080" alt="env" src="https://github.com/user-attachments/assets/805b76ac-1a4f-44b0-a614-7552d757b7d7" />

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mi_base_de_datos
DB_USER=mi_usuario
DB_PASSWORD=mi_password
```

Para usar el proyecto, copia la plantilla y rellena tus datos:

```bash
cp .env.example .env
```

## Construcción de la URL de conexión

Se usa `URL.create()` de SQLAlchemy. Esto es importante porque **maneja correctamente contraseñas con caracteres especiales** como `@`, `%`, `:`, `#`, etc., que romperían una URL construida por concatenación.

### Forma incorrecta (falla con caracteres especiales)

```python
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

### Forma correcta

<img width="1920" height="1080" alt="env" src="https://github.com/user-attachments/assets/e62262be-d14d-42e7-965a-64be355d8fb5" />

```python
from sqlalchemy.engine import URL

url_object = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),  # Se pasa tal cual, sin escapar
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url_object)
```

> El parámetro `password` de `URL.create()` **no requiere codificación URL previa**. Se pasa la contraseña original tal como está escrita.


## Prueba de conexión

<img width="1920" height="1080" alt="prueba_de_conexion" src="https://github.com/user-attachments/assets/a1d6359f-40a4-453a-b521-532bdec20050" />

```bash
python test_conexion.py
```

Si todo está bien configurado, el script debe mostrar la versión de PostgreSQL y un mensaje de éxito.

## Estructura de columnas de una tabla

Para inspeccionar las columnas de la tabla products (nombre, tipo de dato y posición) se puede hacer desde tres enfoques distintos.

### Desde psql
El meta-comando \d muestra la estructura completa de una tabla directamente en la terminal de PostgreSQL:

```bash
\d products
```
<img width="1888" height="1017" alt="describiendo_columnas_psql" src="https://github.com/user-attachments/assets/48cb4858-d56f-4ceb-b46e-cc12d40bc723" />

### Desde SQL puro

Consulta estándar al catálogo del sistema information_schema, portable a otros motores SQL como MySQL o SQL Server:

```sql
SELECT COLUMN_NAME,
       DATA_TYPE,
       ORDINAL_POSITION
FROM information_schema.columns
WHERE table_name = 'products';
```

<img width="1879" height="987" alt="describiendo_columnas_sql" src="https://github.com/user-attachments/assets/eff3e828-efc7-4396-b3b9-c73152003e70" />


### Desde Python con SQLAlchemy

Se ejecuta el mismo SQL usando text() de SQLAlchemy. El parámetro :tabla evita inyección SQL y permite reutilizar el script para otras tablas.

```python
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
```

<img width="1884" height="1000" alt="describiendo_columnas_py" src="https://github.com/user-attachments/assets/3ddba56c-d907-4596-9986-deb4d721ba29" />

Nota sobre sys.path: como el script vive dentro de actividades/02_creating_tables/, se necesita subir dos niveles con parents[2] para llegar a la raíz del proyecto y poder importar config.py.

## Notas adicionales

- **Seguridad:** Si una contraseña real llegó a commitearse o a compartirse, es recomendable cambiarla en PostgreSQL:
  ```bash
  sudo -u postgres psql
  ALTER USER usuario WITH PASSWORD 'nueva_password_segura';
  \q
  ```
