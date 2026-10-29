# PREP-EIME v1.12.0 — Biblioteca mixta

1. Respalda la base de datos y ejecuta `migration_1120_biblioteca_mixta.sql` en Supabase SQL Editor.
2. Sube este código a GitHub y despliega Streamlit.
3. Ingresa como administrador, abre Biblioteca, selecciona un curso, registra un recurso y publícalo.
4. Ingresa como estudiante activo de esa carrera y verifica que solo se muestren recursos publicados.
5. Verifica que los PDF solo abran con enlaces firmados y que estudiantes no puedan modificar recursos.

**Notas:** la biblioteca consulta 20 asociaciones por página. Los PDF se almacenan en Storage privado, no en memoria persistente de Streamlit. La publicación de un PDF se debe hacer después de verificar su carga. El formulario no implementa edición de contenido ni eliminación definitiva; se utiliza archivado. Antes de producción revisar RLS y políticas de Storage con usuarios de prueba.
