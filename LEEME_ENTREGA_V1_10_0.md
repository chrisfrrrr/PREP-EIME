# PREP-EIME v1.10.0 — Diagnóstico estudiantil

## Cambio incluido
En «Mi progreso», el estudiante puede solicitar un diagnóstico por curso y criterio, y visualizar las recomendaciones que el administrador haya publicado. El análisis solo usa los RPC de resultados, rúbricas y retroalimentación publicados, con la autorización vigente de Supabase. No modifica calificaciones ni permisos.

## Instalación
Copiar todos los archivos a GitHub, incluido `modules/student_guidance.py`. No se requieren nuevas migraciones ni secretos.

## Validación imprescindible
1. Estudiante con simulacro pendiente: no debe ver rúbrica, comentarios ni puntuación sin publicar.
2. Estudiante con simulacro publicado: diagnóstico por curso y criterio, recomendaciones cuando existan.
3. Administrador: guardado unificado y navegación dentro del mismo simulacro.
4. Publicación: confirmar que no se publica con criterios incompletos.
5. Descargas: Excel de evaluación y expediente individual.
6. Probar con dos usuarios estudiantes diferentes: cada uno solo ve su información.

## Alcance
Consulta como máximo los 30 simulacros administrativos finalizados más recientes del estudiante al pulsar «Actualizar mi diagnóstico». El 70% es umbral orientativo, no requisito oficial. Las calificaciones históricas de autoevaluación continúan en el historial pero no en este diagnóstico.
