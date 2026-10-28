# PREP-EIME v1.8.0 — Preparación para publicación

## Cambios de esta entrega
- Panel administrativo: vista previa de nota general cuando todas las respuestas están completas.
- Botón de publicación visible pero **deshabilitado** por seguridad.
- `get_attempt()` ahora incluye `grading_mode`, `grading_status` y `published_at`, necesarios para distinguir las modalidades.
- RPC `publish_attempt_grades` conectada en módulo de datos, pero no se invoca desde la interfaz hasta validar permisos.

## Pendientes bloqueantes
1. Restringir INSERT de `attempts` y `attempt_answers`: actualmente un cliente autenticado puede insertar campos de calificación. Revisar la creación de simulacros para retirar del payload `score` y `self_score` nulos y asignar `grading_mode` en el servidor.
2. Bloquear modificaciones de respuestas una vez finalizado el simulacro y transiciones arbitrarias de `attempts.status`.
3. Proteger SELECT de notas administrativas no publicadas. No basta con ocultar componentes Streamlit.
4. Habilitar EXECUTE para authenticated solo tras estas protecciones y pruebas con estudiante/administrador reales.
5. Revisar las rutas heredadas de autoevaluación y cálculo que ya no tienen permiso UPDATE.

No se ha ejecutado ninguna publicación real ni se ha modificado la base de datos desde este paquete.
