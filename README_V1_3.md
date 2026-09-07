# PREP-EIME v1.3 — Gestor Académico

Esta versión agrega escritura académica controlada por rol sobre Supabase.

## Flujo editorial
- Docente: puede editar contenido en `borrador` y `en_revision`, y enviar programas a revisión.
- Coordinador: puede aprobar y publicar.
- Administrador: puede aprobar/publicar y además eliminar unidades/temas.

## Instalación
1. Ejecutar `migration_rls_staff_write_v1_3.sql` en Supabase SQL Editor.
2. Sustituir el contenido del repositorio por esta versión.
3. Conservar los Secrets existentes de Streamlit.
4. Esperar el redeploy automático.
5. Probar Gestión académica.

## Prueba recomendada
Con administrador:
- abrir Gestión académica;
- seleccionar un programa;
- cambiar Borrador → En revisión → Aprobado → Publicado;
- abrir Preparación académica y comprobar que el programa publicado ya es visible.

No se recomienda publicar masivamente todos los programas antes de una revisión académica.
