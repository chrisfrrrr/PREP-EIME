# PREP-EIME v1.7 — Control de calidad y gestión masiva

1. Ejecutar `migration_quality_bulk_v1_7.sql` en Supabase SQL Editor.
2. Actualizar GitHub con el contenido de esta carpeta (app.py, modules/, etc.).
3. Esperar el despliegue de Streamlit. No volver a cargar los 530 registros.
4. Entrar como docente/coordinador y abrir **Control de calidad**.
5. Revisar una pregunta y marcar los cinco criterios; guardar.
6. Entrar como coordinador o administrador y usar **Transiciones masivas**.
7. Seleccionar la pregunta aprobada, pasarla de borrador a en revisión, luego a aprobado y finalmente a publicado.

## Seguridad
- No se permite publicación nueva sin revisión positiva.
- La modificación del contenido invalida su revisión.
- Las transiciones masivas verifican el rol y la etapa en la base de datos.
- Las preguntas anteriores publicadas no se despublican automáticamente.
- Los 530 registros iniciales permanecen en borrador hasta revisión.

**Precaución:** las preguntas generadas para el banco inicial son material de prueba. La aprobación debe ser académica y real, no una marca automática.
