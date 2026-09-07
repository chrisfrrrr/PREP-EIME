# PREP-EIME v1.5 — Simulador EGP

Versión inicial del simulador escrito del Examen General Privado.

## Funcionalidades
- simulacro por carrera;
- selección aleatoria de preguntas publicadas;
- filtros por área y dificultad;
- número de preguntas configurable;
- tiempo sugerido;
- una pregunta a la vez;
- guardado de respuestas en Supabase;
- historial de intentos;
- revisión posterior;
- autoevaluación guiada contra la respuesta esperada;
- diagnóstico por área, curso, competencia y dificultad;
- evolución básica en Mi progreso.

## Por qué v1.5 usa autoevaluación guiada
El banco actual contiene preguntas abiertas, de cálculo, análisis, diseño y defensa
técnica. No es correcto calificarlas mediante coincidencia textual simple.
Por ello, el estudiante responde sin ver la solución y, al finalizar, compara
su desarrollo con el criterio esperado y registra su nivel de cumplimiento.

La estructura queda preparada para incorporar posteriormente:
- opción múltiple y numéricas autocalificables;
- rúbricas;
- revisión docente;
- evaluación asistida por IA;
- simulador oral.

## Instalación
1. Ejecutar `migration_simulator_v1_5.sql` en Supabase SQL Editor.
2. Actualizar el repositorio de GitHub con esta versión.
3. Mantener los Secrets actuales.
4. Probar con una cuenta de estudiante que tenga `career_code`.
5. Se necesitan preguntas `publicado` vinculadas a esa carrera.
