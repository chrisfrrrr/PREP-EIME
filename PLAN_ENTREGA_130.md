# PREP-EIME 1.8.0 — Entrega agrupada, etapa 130

## Cambio incluido
`migration_130_integridad_respuestas.sql` protege respuestas de simulacros finalizados contra ediciones posteriores por estudiantes. No toca datos históricos ni calificaciones.

## Instalación
1. Hacer respaldo de Supabase y conservar el ZIP anterior.
2. Ejecutar `migration_130_integridad_respuestas.sql` en Supabase SQL Editor.
3. Verificar con cuenta de estudiante que puede responder durante un simulacro en progreso, finalizarlo y que no puede modificar sus respuestas después.

## Bloqueadores pendientes antes de habilitar publicación
- Las tablas `attempts` y `attempt_answers` siguen otorgando SELECT de columnas sensibles a `authenticated`; **no activar** `ENABLE_ADMIN_PUBLICATION`.
- Es necesario sustituir todas las lecturas directas de notas por RPC seguras y después revocar los privilegios SELECT sensibles en una misma ventana de despliegue.
- Probar autorización con JWT real de estudiante, no solo con `Success` del editor SQL.
- Probar la publicación con un simulacro completo y verificar que el resultado sea visible solo al estudiante propietario.

**No se declara completada la seguridad ni la publicación.**
