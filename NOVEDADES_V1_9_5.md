# PREP-EIME v1.9.5 — Corrección de navegación administrativa

Se corrigió el cambio inesperado de simulacro y el regreso a la pregunta 1 al usar «Guardar retroalimentación y siguiente» o «Guardar evaluación y siguiente».

- El selector de simulacros mantiene el ID activo, incluso cuando el estado del simulacro modifica el orden de la bandeja.
- Los cambios manuales de simulacro actualizan el estado activo mediante callback.
- La navegación pendiente de pregunta se aplica antes de crear el selector de respuestas y solo se consume en el simulacro correspondiente.
- «Guardar» permanece en la pregunta actual; «Guardar y siguiente» avanza una pregunta.
- No modifica esquema, rúbricas, notas ni permisos. No requiere SQL ni cambios de Secrets.

Validación realizada: compilación Python, integridad del ZIP y pruebas estáticas de las rutas de navegación. Pendiente: prueba funcional con Streamlit y Supabase reales.
