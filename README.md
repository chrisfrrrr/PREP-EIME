
# PREP-EIME v1.0

**Plataforma de Repaso y Evaluación para el Examen General Privado**  
Escuela de Ingeniería Mecánica Eléctrica

Esta primera versión deja lista la columna vertebral del sistema:

- autenticación con Supabase (opcional en modo demo);
- roles: estudiante, docente, coordinador y administrador;
- carreras y cohortes;
- áreas EGP;
- cursos oficiales;
- relación curso-carrera;
- biblioteca;
- banco de preguntas;
- simulador básico;
- progreso;
- paneles diferenciados por rol;
- esquema PostgreSQL/Supabase con RLS base.

## 1. Ejecución rápida en modo demo

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

En modo demo no necesitas Supabase. Usa estas credenciales:

- Estudiante: `estudiante@demo.gt` / `demo123`
- Docente: `docente@demo.gt` / `demo123`
- Coordinación: `coordinacion@demo.gt` / `demo123`
- Administrador: `admin@demo.gt` / `demo123`

## 2. Conectar Supabase

1. Crear un proyecto en Supabase.
2. Ejecutar `supabase_schema.sql` en SQL Editor.
3. Crear un bucket privado llamado `prep-eime`.
4. Copiar `.env.example` a `.env`.
5. Completar:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
6. Cambiar `DEMO_MODE=true` a `DEMO_MODE=false`.

## 3. Estructura

```text
PREP_EIME_v1/
├── app.py
├── requirements.txt
├── .env.example
├── supabase_schema.sql
├── seed_demo.sql
├── modules/
│   ├── auth.py
│   ├── data.py
│   ├── ui.py
│   └── config.py
└── .streamlit/
    └── config.toml
```

## 4. Próxima fase

Cuando se disponga de los programas oficiales de curso:

`programa oficial → unidades → temas → subtemas → contenido → preguntas EGP`

No se recomienda incorporar contenidos académicos no validados como oficiales.
