# PREP-EIME v1.7.3 — Corrección del simulador EGP

## Corrección

- Se agregó la importación faltante `get_published_questions_for_simulator_v16` desde `modules.data` en `app.py`.
- Se conserva la paginación y la interfaz de calidad de la versión v1.7.2.
- No se modifica el esquema, los permisos RLS ni los registros de Supabase.

## Despliegue

Sustituir los archivos del repositorio con los de este ZIP, conservando los secretos configurados en Streamlit Cloud. No ejecutar scripts SQL de migración ni de carga de datos para esta corrección.

## Prueba

Iniciar sesión como estudiante IE e ingresar a Simulador EGP. Debe mostrarse el formulario de configuración con la pregunta publicada de Electrónica 3. No iniciar todavía el simulacro hasta verificar la pantalla.

## Validación local

Sintaxis Python validada con `ast.parse`; importaciones del módulo `modules.data` cotejadas con las definiciones disponibles. No se realizó prueba en vivo con Supabase.
