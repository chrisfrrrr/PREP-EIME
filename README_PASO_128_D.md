# PREP-EIME v1.8.0 — Integración controlada de publicación

1. Ejecute `migration_v1_8_0_publication_result_rpc.sql` en Supabase.
2. Despliegue el proyecto. Verifique que la revisión estudiantil cargue sin errores.
3. La publicación permanece desactivada por defecto (`ENABLE_ADMIN_PUBLICATION` ausente o false).
4. No establezca `ENABLE_ADMIN_PUBLICATION=true` hasta completar y probar los controles de INSERT/UPDATE, las transiciones de estado y la lectura directa de columnas sensibles en las tablas existentes.
5. No se ha probado la conexión real a Supabase desde este entorno.
