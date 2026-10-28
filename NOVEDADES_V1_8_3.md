# PREP-EIME v1.8.3 — Gestión administrativa

## Novedades
- Nombre y carné del estudiante a través de `get_profiles_by_ids` existente; se conserva el fallback si RLS no permite consultar perfiles.
- Fechas de finalización en `America/Guatemala`.
- Filtros por estado, carrera, nombre, carné, UUID y rango de fechas local.
- Prioridad: pendientes antiguos, en evaluación, evaluados, publicados.
- Métricas: respuestas por completar, porcentaje publicado, listos para publicar.
- Exportación CSV UTF-8 BOM para Excel con registros filtrados, notas **solo publicadas** y metadatos de publicación.

## Despliegue
Reemplazar archivos en la misma rama de GitHub usada por Streamlit. No se requieren migraciones SQL ni nuevos Secrets.

## Validación
1. Ingresar como administrador y comprobar que la bandeja muestra nombres/carnés si la política de perfiles lo permite.
2. Filtrar por Pendiente, revisar orden de antigüedad, descargar CSV.
3. Filtrar por Publicado y verificar nota 57.88 del simulacro de cuatro respuestas.
4. Verificar que los estudiantes no tengan acceso a la pantalla administrativa.

## Alcance y límites
La bandeja está limitada a los 200 intentos más recientes, como en v1.8.2. El porcentaje publicado usa esa misma población. Los nombres/carnés requieren acceso autorizado a perfiles. El reporte es CSV compatible con Excel, no XLSX. No se implementó una duración media de evaluación porque no existe una definición de inicio fiable para medirla en el esquema consultado. No se ha probado contra la base de datos de producción.
