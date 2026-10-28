# PREP-EIME v1.9.1

- Administrador: observaciones y recomendaciones por respuesta; guardado independiente de rúbrica.
- Estudiante: retroalimentación visible solo después de publicación oficial.
- Seguridad: RPCs verifican rol, pertenencia, estado de publicación y bloquean cambios posteriores.
- Conserva todas las notas y rúbricas existentes; no modifica el historial.
- Instalación: ejecutar `migration_191_retroalimentacion.sql` UNA SOLA VEZ en Supabase SQL Editor; luego subir el contenido del ZIP a GitHub.
- Los registros ya publicados quedan sin retroalimentación retroactiva; no se reabren.
- Prueba: en un intento no publicado, guardar observación y recomendación; verificar que el estudiante no las ve; publicar y verificar que aparecen en la revisión.
