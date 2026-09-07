# PREP-EIME v1.4 — Banco de Preguntas EGP

Esta versión incorpora un banco institucional de preguntas vinculado a Supabase.

## Qué agrega
- creación de preguntas desde Streamlit;
- vínculo pregunta ↔ curso;
- vínculo opcional pregunta ↔ unidad/tema;
- vínculo pregunta ↔ una o varias carreras;
- dificultad 1–5;
- competencia evaluada;
- tipo de pregunta;
- respuesta esperada / criterio;
- flujo borrador → en revisión → aprobado → publicado;
- filtros por carrera, área, estado y dificultad;
- lectura de preguntas publicadas desde Preparación EGP.

## Flujo editorial
Docente:
- crea y edita borradores;
- envía a revisión.

Coordinador:
- revisa;
- aprueba;
- publica.

Administrador:
- mismas capacidades que coordinación;
- puede eliminar preguntas.

## Instalación
1. Ejecutar `migration_rls_question_bank_v1_4.sql` en Supabase SQL Editor.
2. Sustituir la versión v1.3 del repositorio por v1.4.
3. No cambiar los Secrets de Streamlit.
4. Esperar el redeploy.
5. Entrar como administrador a Banco de preguntas.
6. Crear una pregunta piloto.
7. Llevarla a Publicado.
8. Revisarla desde Preparación EGP seleccionando una carrera asociada.

## Recomendación
No cargar grandes cantidades de preguntas hasta validar primero el flujo con 3–5 preguntas piloto.
