# PREP-EIME v1.8.2 — Panel de gestión de evaluaciones

## Incluye
- Contadores de pendientes, en evaluación, evaluados y publicados.
- Filtros por estado y carrera, búsqueda por ID de estudiante o simulacro.
- Bandeja con fecha de finalización, respuestas completas y porcentaje de avance.
- Selección de simulacro desde la bandeja y acceso a la evaluación existente.
- Consultas por lotes, sin cambios de esquema ni migraciones SQL.

## Instalación y prueba
Despliega el ZIP en Streamlit. No ejecutes SQL nuevo. Accede como administrador activo a «Evaluación administrativa». Comprueba que los contadores y la tabla aparecen, filtra por «Publicado» y abre el simulacro ya publicado. Luego filtra por «Pendiente» y abre otro simulacro. La evaluación y publicación anteriores deben permanecer intactas.

## Limitaciones
La bandeja muestra los últimos 200 simulacros administrativos finalizados, no es un reporte histórico completo. El campo estudiante muestra el prefijo de su UUID, no su nombre; no se amplían permisos de perfiles. La trazabilidad detallada por evaluador queda pendiente de un módulo de auditoría. Los bloqueos de seguridad instalados siguen requiriendo pruebas reales de roles para producción.
