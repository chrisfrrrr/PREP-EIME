# PREP-EIME v1.6.1 — Banco inicial de 530 preguntas

Se agregan 530 preguntas de prueba: 10 para cada uno de los 53 cursos técnicos
del núcleo EGP.

## Carga
1. Debe estar instalada la migración de v1.6.
2. Ejecutar en Supabase SQL Editor:
   `seed_banco_530_preguntas_v1_6_1.sql`
3. El seed es idempotente: utiliza UUID deterministas y `ON CONFLICT(id)`.
4. Todas las preguntas quedan en `borrador`. Deben revisarse antes de publicarse.

## Distribución por curso
Cada curso recibe:
- 6 preguntas de autoevaluación guiada;
- 4 preguntas con rúbrica/revisión académica;
- dificultades entre 2 y 5;
- competencias Explicar, Calcular, Analizar, Diseñar/Seleccionar y Defender técnicamente;
- pesos entre 1.0 y 2.5.

No se generaron respuestas autocalificables ficticias. Las preguntas automáticas
requieren valores u opciones técnicamente validados por un docente.

## Asociación a unidades
La mayoría de preguntas queda asociada a unidades reales ya cargadas en `topics`.
En la base académica actual hay 7 cursos del núcleo sin
registros de `topics`, por lo que sus preguntas quedan asociadas al curso, con
`topic_id = NULL`, para no inventar unidades oficiales.

Cursos afectados:
- 0250 · Mecánica de Fluidos
- 0252 · Hidráulica
- 0258 · Máquinas Hidráulicas
- 0390 · Termodinámica 1
- 0524 · Diseño de Máquinas 1
- 0526 · Diseño de Máquinas 2
- 0532 · Vibraciones

El CSV `Banco_530_Preguntas_REVISION.csv` permite revisar rápidamente todo el banco.
