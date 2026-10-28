# Paso 129-F — Protección de presentación en Mi progreso

- El historial y Mi progreso ahora usan el mismo filtro de publicación administrativa.
- La calificación administrativa no publicada no contribuye al promedio, tabla ni gráficos del estudiante.
- Si falla la RPC, la nota administrativa permanece oculta (fail closed).
- Se conservan los resultados históricos y la interfaz de evaluación administrativa.

## Limitación crítica

Esto **NO** revoca el acceso directo a `attempts.score` ni a los campos de evaluación de `attempt_answers`. NO habilitar `ENABLE_ADMIN_PUBLICATION` todavía. La siguiente migración debe trasladar las consultas de estudiantes y personal a RPCs separadas antes de revocar permisos SELECT sobre columnas sensibles.

## Prueba recomendada

1. Instalar esta versión en Streamlit.
2. Como estudiante, abrir Historial y Mi progreso: un simulacro administrativo pendiente debe mostrar Pendiente y no entrar al promedio.
3. Como administrador, confirmar que siguen visibles las cuatro respuestas del simulacro más reciente.
4. No ejecutar SQL ni habilitar publicación en este paso.
