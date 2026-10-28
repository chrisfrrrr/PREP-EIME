# PREP-EIME v1.9.4 — Corrección de estado de widgets Streamlit

Corrige el error `st.session_state['admin_queue_selected'] cannot be modified after the widget with that key is instantiated` al guardar retroalimentación o rúbricas.

- No modifica el estado de los selectbox después de renderizarlos.
- Conserva simulacro y pregunta al guardar sin avanzar.
- Para «Guardar y siguiente» y navegación manual, prepara el cambio y lo aplica antes de crear el widget en el siguiente rerun.
- No requiere migración SQL ni cambios en Secrets.

Validación: sintaxis de Python compilada. Es necesario probar el comportamiento en Streamlit conectado a Supabase.
