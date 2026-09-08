# PREP-EIME v1.6 — Evaluación estructurada

Esta versión amplía el simulador para distinguir tres modalidades de evaluación:

1. Autocalificable
   - Opción múltiple.
   - Respuesta numérica con tolerancia absoluta.

2. Autoevaluación guiada
   - Respuesta abierta.
   - Problemas de cálculo o explicación cuando el equipo académico decida mantener revisión personal.

3. Rúbrica / revisión docente
   - Análisis de caso.
   - Diseño / selección.
   - Defensa técnica.
   - Otras respuestas abiertas de alta complejidad.

## Nuevos campos en questions
- evaluation_mode
- answer_config JSONB
- rubric JSONB
- weight

## Nuevos campos en attempt_answers
- auto_score
- review_score
- reviewed_by
- reviewed_at

## Flujo de prueba recomendado

1. Ejecutar `migration_structured_evaluation_v1_6.sql`.
2. Actualizar GitHub con v1.6.
3. Crear tres preguntas piloto:
   - una de Opción múltiple;
   - una de Respuesta numérica;
   - una de Análisis de caso con rúbrica.
4. Publicarlas.
5. Entrar como estudiante y realizar un simulacro.
6. Verificar que opción múltiple y numérica se califican automáticamente.
7. Verificar que la de rúbrica aparece pendiente.
8. Entrar como docente/coordinador/admin a `Revisión de respuestas`.
9. Calificar la respuesta pendiente.
10. Volver como estudiante y comprobar que el resultado se actualizó.

## Nota académica
Las preguntas publicadas previamente conservan `autoevaluacion` para evitar asumir
una respuesta correcta estructurada que no fue definida explícitamente.
