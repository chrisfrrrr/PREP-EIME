# PREP-EIME v1.2

Esta versión sustituye el catálogo académico demostrativo por lecturas reales desde Supabase.

## Antes de desplegar
1. Ejecutar `migration_rls_staff_read_v1_2.sql` una sola vez en Supabase SQL Editor.
2. Mantener en Streamlit Secrets:
   - `DEMO_MODE = "false"`
   - `SUPABASE_URL`
   - `SUPABASE_KEY` (anon/publishable, nunca service_role)
3. Reemplazar los archivos del repositorio por los de esta carpeta y hacer push a GitHub.
4. Streamlit Community Cloud redeployará automáticamente.

## Qué cambia
- La sesión de Supabase se conserva para que RLS funcione en lecturas posteriores al login.
- Cursos y áreas se leen desde `courses`, `career_courses`, `egp_areas`.
- Personal académico puede revisar programas y temas en borrador.
- Estudiantes solo ven programas/temas `publicado`.
- Gestión académica v1.2 es de lectura/revisión; todavía no edita la base.
