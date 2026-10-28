# Etapa 132 — Continuidad de evaluación administrativa

Se corrigió el selector de respuestas para conservar la pregunta actual después de guardar una rúbrica. La selección se almacena por ID de respuesta y simulacro en `st.session_state`.

## Publicación
La opción `ENABLE_ADMIN_PUBLICATION` permanece desactivada. Antes de activarla se debe probar con una sesión real de estudiante que `publish_attempt_grades` rechaza la operación, y verificar la definición de la función con la migración 131. No se han realizado pruebas en Supabase desde este entorno.

## Prueba rápida
Como administrador, abrir un simulacro, seleccionar la respuesta 3, modificar una valoración y guardar. Debe permanecer seleccionada la respuesta 3.
