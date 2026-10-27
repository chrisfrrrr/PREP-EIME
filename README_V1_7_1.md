# PREP-EIME v1.7.1 — Corrección de consultas paginadas

## Alcance
Se actualizó exclusivamente `modules/data.py` para evitar truncamientos de consultas PostgREST/Supabase cuando una tabla supera 1,000 filas.

- Recuperación paginada de bancos de preguntas en ambas versiones de `get_all_questions`.
- Recuperación paginada de `question_careers` para visualizar todas las carreras asociadas.
- Recuperación paginada de asociaciones y consultas de preguntas por lotes de 200 IDs para los simuladores y consultas por carrera.
- Recuperación paginada de revisiones de control de calidad.
- Los errores de consulta se propagan; no se presenta un conjunto parcial como si estuviera completo.

## Despliegue
1. Respalda tu repositorio actual.
2. Reemplaza `modules/data.py` por el de esta versión, o actualiza el repositorio con el ZIP completo.
3. No ejecutes los archivos de migración ni los scripts `seed_*.sql` del repositorio: no son necesarios para esta corrección.
4. Reinicia/redeploy la aplicación Streamlit.
5. En **Control de calidad EGP**, verifica: 1,080 preguntas, 0 revisadas y 1,080 pendientes (si no existen revisiones de calidad previas).
6. En **Banco de preguntas**, comprueba el total y las asociaciones de carreras; verifica un curso con 30 preguntas.
7. Realiza pruebas de revisión, publicación y simulador con un conjunto pequeño y controlado, sin publicar masivamente el banco.

## Notas
- La base de datos debe seguir con 59 cursos, 36 bancos completos, 1,080 preguntas en borrador y 2,070 asociaciones.
- El recuento de revisiones depende de los registros reales de `question_quality_reviews`.
- Se verificó la sintaxis de los módulos Python y la lógica de paginación mediante pruebas simuladas; no se dispone de credenciales para realizar pruebas de integración contra Supabase.
