# PREP-EIME v1.7.8 — filtro por unidad temática

En **Preparación EGP** se agrega el filtro dependiente **Unidad temática**:

- El estudiante selecciona Área y Curso; Unidad temática ofrece las unidades publicadas con preguntas publicadas asociadas al curso.
- «Todas» mantiene las 30 preguntas del curso cuando se selecciona un banco completo.
- La selección de unidad filtra por `questions.topic_id` (UUID), sin mezclar cursos ni carreras.
- Al cambiar de área o curso, la unidad se reinicia automáticamente.
- El filtro de Dificultad sigue funcionando conjuntamente.
- Si Curso es «Todos», el filtro de unidad queda deshabilitado.

No se requieren cambios en Supabase. Verificar funcionalmente en Streamlit con el curso 0236, unidad «Diagramas de Bloques»: se esperan 5 preguntas antes de aplicar dificultad.
