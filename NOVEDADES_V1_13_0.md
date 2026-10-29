# PREP-EIME v1.13.0 — optimización y acabado profesional

## Mejoras incluidas
- Identidad visual uniforme, espaciado responsivo, controles primarios y menú con iconos.
- Encabezados y métricas con contenido HTML escapado para evitar inyección accidental.
- Inicio con accesos rápidos a simulador, biblioteca y progreso, sin consultas adicionales.
- Navegación segura entre secciones mediante cambio diferido de session_state, evitando el error de modificación de widgets ya instanciados.
- Corrección de la apertura de PDF: el enlace firmado persiste durante su corta vigencia y no desaparece por el rerun inmediato de Streamlit.
- Versión visible 1.13.0.

## Instalación
1. Guardar copia del repositorio actualmente desplegado.
2. Sustituir los archivos del proyecto por los del ZIP, conservando secretos en Streamlit Cloud.
3. Publicar en GitHub y reiniciar la aplicación.
4. Verificar inicio de sesión, navegación, biblioteca, apertura de PDF, simulador, evaluación administrativa y resultados publicados.

**No requiere migración SQL ni cambios en Supabase.** No se alteran preguntas, intentos, respuestas, rúbricas ni notas. No se incorporan dependencias.

## Límites de validación
Se valida compilación de Python y contenido del paquete; no es posible probar aquí credenciales reales, permisos RLS ni ejecución sobre el proyecto Supabase de producción.
