# PREP-EIME v1.8.0 — Paso 129-G

- Se corrige la columna Resultado de Mi progreso: ya no muestra `None`.
- Las notas administrativas sin publicar se presentan como texto, no como cero.
- El promedio y la gráfica continúan usando únicamente intentos con nota visible.
- No se alteran las tablas ni los permisos de Supabase.
- La publicación administrativa continúa deshabilitada.

## Pendiente de seguridad

Los SELECT actuales de `attempts` y `attempt_answers` siguen leyendo columnas sensibles.
Antes de revocar privilegios hay que migrar las lecturas a RPC de consulta controlada y
probarlas tanto con cuenta estudiante como administrador. Esta versión NO resuelve
por sí sola la exposición directa vía API.
