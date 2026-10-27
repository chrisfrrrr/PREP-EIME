# PREP-EIME v1.7.4 — Corrección del historial del simulador

- Se implementó `_attempt_history(user)` en `app.py`, que estaba invocada desde el simulador y Mi progreso sin definición.
- El historial presenta fecha, estado, cantidad de preguntas y resultado.
- Permite abrir un simulacro finalizado en la pantalla de revisión existente.
- No modifica tablas, RLS, autenticación, preguntas ni transiciones.
- Se conserva la importación corregida en v1.7.3 y la paginación de v1.7.1.

**Prueba recomendada:** iniciar sesión como estudiante IE y abrir Simulador EGP; debe aparecer la configuración y un historial vacío, sin NameError. Luego iniciar un simulacro con la única pregunta publicada y comprobar el flujo.
