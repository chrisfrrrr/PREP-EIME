# PREP-EIME 1.8.0 — Etapa 131

Esta entrega añade tres controles en la base de datos: impide notas administrativas en `attempts.score` antes de publicación, impide altas y bajas de respuestas finalizadas, e impide guardar puntuaciones administrativas en campos históricos de `attempt_answers`.

## Despliegue

1. Respalda Supabase y conserva la versión anterior del ZIP.
2. Ejecuta `migration_131_integridad_publicacion.sql` en SQL Editor.
3. Verifica con JWT real de estudiante que no puede modificar respuestas finalizadas ni publicar.
4. Verifica con administrador que las cuatro respuestas se pueden evaluar y que la función de publicación admite las notas completas.
5. **Solo después de verificar la autorización y publicación**, configura en Streamlit Secrets: `ENABLE_ADMIN_PUBLICATION = true`.
6. Comprueba la nota en historial, Mi progreso y revisión con el estudiante propietario y que otro estudiante no puede consultarla.

## Limitaciones

- No se revocan los SELECT históricos: la confidencialidad administrativa se basa en no almacenar notas en las tablas originales antes de publicar. Las rúbricas deben mantener RLS administrador.
- No se verificaron datos existentes ni la definición real de la función de publicación en tu Supabase. Si hay notas administrativas preexistentes en tablas originales, deben revisarse.
- El disparador de Etapa 130 todavía permite a un administrador cambiar el texto de una respuesta finalizada. Debe endurecerse antes de producción.
- No se ejecutaron pruebas de integración con Supabase.
