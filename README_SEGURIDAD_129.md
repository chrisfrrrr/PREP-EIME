# PREP-EIME v1.8.0 — Entrega de transición 129

## Cambios comprobables
- Historial estudiantil: calificaciones de simulacros administrativos solo desde `get_my_published_attempt_result`, nunca desde el campo `attempts.score`. Ante error de la RPC se muestra pendiente.
- Revisión: el aviso de pendiente desaparece tras publicación oficial.
- Revisión histórica: se elimina el recálculo de nota ejecutado solo por abrir la pantalla.
- Publicación administrativa sigue desactivada mediante `ENABLE_ADMIN_PUBLICATION=False`.

## IMPORTANTE: pendiente de seguridad en Supabase
Este paquete NO revoca permisos de lectura sobre `attempts.score` y `attempt_answers.score/review_score/feedback`, por lo que NO garantiza confidencialidad ante llamadas directas a Supabase. NO activar la publicación. Antes de revocar columnas hay que migrar las lecturas en `get_attempt`, `get_attempt_answers_v16`, `get_student_attempts`, y las pantallas de progreso, además de confirmar las dependencias de las consultas históricas. La RPC de consulta publicada debe estar instalada.

## Pruebas
Validación estática de Python y estructura ZIP. No se dispone de conexión a Supabase para pruebas de integración.
