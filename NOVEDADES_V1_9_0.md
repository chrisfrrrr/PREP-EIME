# PREP-EIME v1.9.0 — Expedientes y analítica académica

## Incluye
- Expediente administrativo individual: estudiante, carné, carrera, historial de simulacros administrativos, estado, respuestas evaluadas y nota oficial.
- Promedio individual calculado **solo** con resultados administrativos publicados.
- Gráfico de evolución para estudiantes con dos o más notas publicadas.
- Exportación del expediente individual a Excel, con hojas «Expediente» y «Resumen».
- Analítica de carrera: estudiantes distintos, simulacros, resultados publicados y promedio de notas publicadas.
- Gráfico de promedios publicados por carrera.

## Despliegue
1. Reemplaza el proyecto en GitHub, **incluida la nueva carpeta/archivo `modules/academic_analytics.py`**.
2. Espera a que Streamlit vuelva a desplegar.
3. Ingresa como administrador, abre «Evaluación administrativa» y expande «Expedientes y analítica académica · v1.9.0».
4. Prueba la descarga Excel del expediente de un estudiante y revisa la pestaña «Analítica académica».

## Seguridad y alcance
- No requiere SQL ni Secrets nuevos; conserva el control de acceso administrativo existente.
- No cambia las rúbricas, notas, permisos ni el proceso de publicación.
- La analítica solo considera los **hasta 200 simulacros administrativos finalizados más recientes** devueltos por la bandeja existente; no es un censo histórico completo.
- No incluye notas históricas de autoevaluación. Las notas administrativas pendientes permanecen sin valor numérico.
- No amplía el acceso de docentes.
- El nombre y carné dependen de los permisos de lectura de perfiles existentes.

## Validación
Se comprobó la sintaxis de los módulos Python y la integridad del ZIP. No se realizó una prueba contra la instancia real de Supabase.
