-- PREP-EIME v1.12.0 Biblioteca mixta. Ejecutar con rol postgres tras respaldo.
BEGIN;
CREATE TABLE IF NOT EXISTS public.library_resources (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 title text NOT NULL CHECK (char_length(trim(title)) BETWEEN 4 AND 180),
 description text NOT NULL DEFAULT '',
 resource_type text NOT NULL CHECK (resource_type IN ('guia','documento','bibliografia','enlace')),
 author text NOT NULL DEFAULT '', publication_year integer CHECK (publication_year BETWEEN 1800 AND 2100),
 url text CHECK (url IS NULL OR (url ~ '^https://[^[:space:]]+$' AND length(url) <= 2000)),
 storage_path text UNIQUE CHECK (storage_path IS NULL OR (storage_path ~ '^[a-zA-Z0-9/_-]+\.pdf$' AND length(storage_path) <= 250)),
 unit_label text NOT NULL DEFAULT '',
 status text NOT NULL DEFAULT 'borrador' CHECK (status IN ('borrador','publicado','archivado')),
 created_by uuid REFERENCES public.profiles(id),
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
 CHECK (url IS NOT NULL OR storage_path IS NOT NULL OR resource_type IN ('guia','bibliografia'))
);
CREATE TABLE IF NOT EXISTS public.library_resource_courses (
 resource_id uuid NOT NULL REFERENCES public.library_resources(id) ON DELETE CASCADE,
 course_code text NOT NULL REFERENCES public.courses(code),
 PRIMARY KEY(resource_id,course_code)
);
CREATE INDEX IF NOT EXISTS library_resources_status_idx ON public.library_resources(status,created_at DESC);
CREATE INDEX IF NOT EXISTS library_resource_courses_course_idx ON public.library_resource_courses(course_code,resource_id);
CREATE OR REPLACE FUNCTION public.prep_library_admin() RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path='' AS $$
 SELECT EXISTS (SELECT 1 FROM public.profiles p JOIN auth.users u ON u.id=p.id WHERE p.id=(SELECT auth.uid()) AND p.role::text='administrador' AND p.status='activo' AND u.email_confirmed_at IS NOT NULL);
$$;
CREATE OR REPLACE FUNCTION public.prep_library_student() RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path='' AS $$
 SELECT EXISTS (SELECT 1 FROM public.profiles p JOIN auth.users u ON u.id=p.id WHERE p.id=(SELECT auth.uid()) AND p.role::text='estudiante' AND p.status='activo' AND u.email_confirmed_at IS NOT NULL);
$$;
REVOKE ALL ON FUNCTION public.prep_library_admin() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.prep_library_student() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.prep_library_admin(),public.prep_library_student() TO authenticated;
CREATE OR REPLACE FUNCTION public.prep_library_can_read(p_resource uuid)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path='' AS $$
 SELECT public.prep_library_admin() OR (public.prep_library_student() AND EXISTS (
 SELECT 1 FROM public.library_resources r
 JOIN public.library_resource_courses lrc ON lrc.resource_id=r.id
 JOIN public.career_courses cc ON cc.course_code=lrc.course_code
 JOIN public.profiles p ON p.career_code=cc.career_code
 WHERE r.id=p_resource AND r.status='publicado' AND p.id=(SELECT auth.uid()) AND cc.is_egp_required=true));
$$;
REVOKE ALL ON FUNCTION public.prep_library_can_read(uuid) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.prep_library_can_read(uuid) TO authenticated;
ALTER TABLE public.library_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.library_resource_courses ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS library_resource_read ON public.library_resources;
CREATE POLICY library_resource_read ON public.library_resources FOR SELECT TO authenticated
USING (public.prep_library_can_read(id));
DROP POLICY IF EXISTS library_resource_write ON public.library_resources;
CREATE POLICY library_resource_write ON public.library_resources FOR ALL TO authenticated USING (public.prep_library_admin()) WITH CHECK (public.prep_library_admin());
DROP POLICY IF EXISTS library_link_read ON public.library_resource_courses;
CREATE POLICY library_link_read ON public.library_resource_courses FOR SELECT TO authenticated
USING (public.prep_library_can_read(resource_id));
DROP POLICY IF EXISTS library_link_write ON public.library_resource_courses;
CREATE POLICY library_link_write ON public.library_resource_courses FOR ALL TO authenticated USING (public.prep_library_admin()) WITH CHECK (public.prep_library_admin());
GRANT SELECT,INSERT,UPDATE,DELETE ON public.library_resources,public.library_resource_courses TO authenticated;
-- Storage: bucket privado; el cliente usa URLs firmadas para lectura.
INSERT INTO storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
VALUES ('prep-library','prep-library',false,10485760,ARRAY['application/pdf'])
ON CONFLICT (id) DO UPDATE SET public=false,file_size_limit=10485760,allowed_mime_types=ARRAY['application/pdf'];
DROP POLICY IF EXISTS prep_library_storage_select ON storage.objects;
CREATE POLICY prep_library_storage_select ON storage.objects FOR SELECT TO authenticated USING (
 bucket_id='prep-library' AND EXISTS (
 SELECT 1 FROM public.library_resources r
 WHERE r.storage_path=storage.objects.name AND public.prep_library_can_read(r.id)));
DROP POLICY IF EXISTS prep_library_storage_insert ON storage.objects;
CREATE POLICY prep_library_storage_insert ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id='prep-library' AND public.prep_library_admin());
DROP POLICY IF EXISTS prep_library_storage_delete ON storage.objects;
CREATE POLICY prep_library_storage_delete ON storage.objects FOR DELETE TO authenticated USING (bucket_id='prep-library' AND public.prep_library_admin());
COMMIT;
