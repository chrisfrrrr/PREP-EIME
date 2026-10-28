# PREP-EIME v1.8.1 — Consolidación

**Cambios:** panel administrativo muestra la nota oficial almacenada cuando ya está publicada; revisión estudiantil presenta el desglose por rúbrica después de publicar; migración de bloqueo de rúbricas y nota publicada.

**Instalación:** respalda Supabase; ejecuta `migration_181_consolidacion.sql`; despliega este ZIP. Conserva `ENABLE_ADMIN_PUBLICATION = true` solo para administradores autorizados.

**Validación integral:** inicia sesión como estudiante propietario del intento publicado, abre Revisión del simulacro y confirma que cada pregunta muestre rúbrica, criterios y puntos. Comprueba que intentos no publicados sigan sin nota ni desglose. En administración confirma que aparezca «Nota oficial publicada».

**Seguridad:** la RPC de desglose valida `auth.uid()` y estado `publicado`. Los triggers impiden editar rúbricas y notas publicadas. Esto no reemplaza pruebas reales de RLS, ni restringe todas las columnas históricas de SELECT. Se recomienda probar con dos cuentas de estudiantes y una de administrador antes de producción.

**Precaución:** si el esquema de Supabase difiere del utilizado en la aplicación, la migración puede necesitar ajustes; no fue ejecutada contra la base real.
