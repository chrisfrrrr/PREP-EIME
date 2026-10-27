# PREP-EIME v1.7.9 — corrección de navegación desde Mi progreso

- Se asigna `key="main_navigation"` al selector lateral de Streamlit.
- El botón **Ver revisión del simulacro** ahora utiliza un callback que selecciona **Simulador EGP** y establece `review_attempt_id` antes de que se reconstruya la interfaz.
- La revisión existente se reutiliza sin alterar el modelo de datos, las calificaciones ni las políticas RLS.
- No requiere migraciones SQL.

## Prueba manual

Con un estudiante, abrir **Mi progreso**, seleccionar un simulacro finalizado y presionar **Ver revisión del simulacro**. Debe cambiar a **Simulador EGP** y mostrar la revisión del intento seleccionado. Comprobar las respuestas y calificaciones históricas. Presionar **Volver al simulador** y confirmar el regreso a la vista del simulador.
