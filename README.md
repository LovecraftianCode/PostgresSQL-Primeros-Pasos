# Conexión a PostgreSQL con Python

Práctica personal de conexión a una base de datos PostgreSQL desde Python usando SQLAlchemy, psql y psycopg2.

## 🛠️ Entorno

- **Sistema operativo:** Arch Linux
- **Shell:** Bash (`/usr/bin/bash`)
- **Base de datos:** PostgreSQL
- **Cliente gráfico:** DBeaver
- **Editor:** Visual Studio Code

## 📦 Dependencias

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
└── test_conexion.py      # Script de prueba de conexión
```

## Carga de la base de datos de ejemplo (SQL for Data Analytics)

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

## Notas adicionales

- **Seguridad:** Si una contraseña real llegó a commitearse o a compartirse, es recomendable cambiarla en PostgreSQL:
  ```bash
  sudo -u postgres psql
  ALTER USER usuario WITH PASSWORD 'nueva_password_segura';
  \q
  ```
