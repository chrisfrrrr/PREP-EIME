# PREP-EIME v1.6.2 — Ajuste académico + banco de 530 preguntas

Esta revisión corrige los 7 cursos que en v1.6.1 no tenían unidades en `topics`:

- 0250 Mecánica de Fluidos
- 0252 Hidráulica
- 0258 Máquinas Hidráulicas
- 0390 Termodinámica 1
- 0524 Diseño de Máquinas 1
- 0526 Diseño de Máquinas 2
- 0532 Vibraciones

Las unidades fueron normalizadas contra programas de curso USAC y la estructura
académica disponible. El nuevo seed utiliza los mismos UUID del banco v1.6.1 y
asocia las preguntas de esos siete cursos a sus unidades.

## Orden correcto de ejecución en Supabase

### Si YA ejecutaste la migración de v1.6
1. Ejecutar `01_ajuste_unidades_7_cursos_v1_6_2.sql`
2. Ejecutar `02_seed_banco_530_preguntas_CORREGIDO_v1_6_2.sql`

### Si TODAVÍA NO ejecutaste la migración de v1.6
1. Ejecutar `migration_structured_evaluation_v1_6.sql`
2. Ejecutar `01_ajuste_unidades_7_cursos_v1_6_2.sql`
3. Ejecutar `02_seed_banco_530_preguntas_CORREGIDO_v1_6_2.sql`

## Resultados esperados
El segundo script contiene tres verificaciones:
- preguntas_seed_530 = 530
- 53 cursos con cantidad = 10
- preguntas_sin_unidad_en_7_cursos = 0

Todas las 530 preguntas quedan en `borrador`.

## Importante
Si ya habías ejecutado el seed v1.6.1, no es necesario borrar nada.
Ejecuta primero el ajuste y después el seed corregido. Al conservar los mismos UUID,
las preguntas se actualizan en lugar de duplicarse.
