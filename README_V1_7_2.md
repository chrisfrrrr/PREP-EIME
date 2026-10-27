# PREP-EIME v1.7.2 — Interfaz de control de calidad EGP

## Cambios
- Sustituye el bloque JSON de `answer_config` por una **Guía de evaluación oral** con etiquetas académicas.
- Presenta unidad, número de pregunta, modalidad, bloque temático, desarrollo en pizarrón, preguntas complementarias y errores críticos cuando existen.
- Mantiene compatibilidad visual con configuraciones de opción múltiple y respuesta numérica.
- Mejora el formulario de revisión con barra de criterios cumplidos y observaciones académicas.
- Mantiene sin cambios la persistencia de revisiones, la lógica de aprobación y la publicación: **guardar una revisión no publica una pregunta**.
- Conserva las correcciones de paginación de v1.7.1.

## Despliegue
1. Respalda el repositorio.
2. Sustituye `app.py` por el de este ZIP (o actualiza el proyecto completo).
3. No ejecutes migraciones SQL ni scripts de carga incluidos en el repositorio.
4. Despliega en Streamlit y verifica la sección Control de calidad EGP.
5. Confirma que se muestren 1,080 preguntas y que la guía oral no muestre JSON.
6. Antes de guardar revisiones reales, verifica la correspondencia entre la rúbrica y la respuesta esperada.

## Validación
- Compilación de archivos Python correcta.
- No se ejecutaron pruebas contra Supabase ni pruebas de interfaz en navegador.
