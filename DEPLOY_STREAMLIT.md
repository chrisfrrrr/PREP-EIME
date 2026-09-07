
# Publicación de PREP-EIME en Streamlit Community Cloud

## Main file path
Usa:

app.py

## Secrets para probar ahora (modo demo)

```toml
DEMO_MODE = "true"
APP_NAME = "PREP-EIME"
SUPABASE_URL = ""
SUPABASE_KEY = ""
```

## Secrets cuando conectes Supabase

```toml
DEMO_MODE = "false"
APP_NAME = "PREP-EIME"
SUPABASE_URL = "https://TU-PROYECTO.supabase.co"
SUPABASE_KEY = "TU_ANON_PUBLIC_KEY"
```

Usa la clave pública/anon del proyecto para la aplicación cliente.
No coloques contraseñas personales dentro del repositorio GitHub.

## Archivos que deben estar en GitHub

- app.py
- requirements.txt
- modules/
- .streamlit/config.toml

También puedes guardar:
- supabase_schema.sql
- seed_demo.sql
- README.md

No subas:
- .env real
- contraseñas
- claves privadas
