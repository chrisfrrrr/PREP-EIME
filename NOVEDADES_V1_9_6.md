# PREP-EIME v1.9.6 — Guardado unificado

- Se unifican la rúbrica y la retroalimentación en un solo formulario por pregunta.
- «Guardar todo y permanecer» guarda ambos componentes y mantiene la pregunta.
- «Guardar todo y siguiente pregunta» guarda ambos y avanza dentro del mismo simulacro.
- Si falla cualquiera de las operaciones no avanza. Si falla la retroalimentación después de guardar la rúbrica, se informa explícitamente para reintentar.
- La última pregunta permanece seleccionada después del guardado.
- No requiere migraciones SQL ni cambios en Secrets.

**Prueba funcional necesaria:** evaluar pregunta 1, guardar y siguiente, confirmar pregunta 2 del mismo simulacro; repetir; probar permanecer y última pregunta.
