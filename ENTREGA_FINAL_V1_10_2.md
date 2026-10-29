# PREP-EIME v1.10.2 — Entrega estabilizada

## Corrección principal
- Se conserva el identificador del simulacro aunque cambie el estado de la evaluación o se reordene la bandeja.
- La lista de opciones del selector de simulacro se mantiene estable por ID, no por posición.
- La navegación entre respuestas utiliza el ID de cada pregunta. «Guardar todo y siguiente» debe recorrer 1→2→3→… sin cambiar de simulacro.
- «Guardar todo y permanecer» conserva la pregunta actual. La última pregunta no avanza.

## Reducción de consumo de RAM
- El Excel administrativo se genera solo al activar «Preparar descarga Excel».
- Los expedientes y la analítica administrativa se consultan solo al activar «Cargar expedientes y analítica».
- Se conservan las limitaciones de consultas y dependencias de la v1.10.1.

## Instalación
1. Subir el contenido de PREP-EIME-main/ al repositorio GitHub (incluido modules/admin_navigation.py).
2. Reiniciar una vez Streamlit Cloud después del despliegue.
3. No ejecutar migraciones SQL ni cambiar Secrets.

## Prueba de aceptación
- Elegir un simulacro de al menos 5 preguntas y pulsar «Guardar todo y siguiente pregunta» tres veces consecutivas.
- Verificar que cambia 1→2→3→4 dentro del MISMO simulacro.
- Verificar que «Guardar todo y permanecer» conserva la pregunta.
- Comprobar publicación, lectura del estudiante y Excel bajo demanda.

## Alcance de la validación
Se comprobó compilación de todos los módulos Python y pruebas automatizadas de la lógica de navegación. La prueba real contra Supabase y Streamlit Cloud requiere ejecución en el entorno del usuario. No se alteran datos de Supabase.
