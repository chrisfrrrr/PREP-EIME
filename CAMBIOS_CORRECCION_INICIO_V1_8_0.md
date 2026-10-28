# Corrección del inicio de simulacros — PREP-EIME v1.8.0

Base: PREP-EIME-v1.8.0-vista-previa-publicacion.zip.

- `create_attempt()` ya no envía `score`, `self_score` ni `evaluation_status` al insertar `attempt_answers`. Esos campos estaban bloqueados por los permisos INSERT por columna aplicados en Supabase.
- Los nuevos intentos se identifican como `grading_mode=administrativa`, `grading_status=pendiente`.
- Los metadatos de los nuevos intentos señalan `evaluation_mode=evaluacion_administrativa`.
- Se actualiza el subtítulo del simulador.
- No se modifican registros históricos ni se habilita publicación.

**Importante:** verificar que `public.attempt_answers.evaluation_status` tenga DEFAULT 'pendiente' en Supabase.
**Seguridad pendiente:** controlar transiciones de estados, lecturas de notas, inserciones iniciales y publicación administrativa.
**Prueba:** crear un simulacro nuevo, avanzar, regresar, finalizar, y confirmar su aparición en Evaluación administrativa.
