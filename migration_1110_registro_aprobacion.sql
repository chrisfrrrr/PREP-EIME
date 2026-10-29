-- PREP-EIME v1.11.0: registro institucional sujeto a aprobación.
-- Ejecutar una sola vez en Supabase SQL Editor con rol postgres.
-- No altera las cuentas preexistentes.
BEGIN;

CREATE OR REPLACE FUNCTION public.prep_validate_signup_domain()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
  IF lower(coalesce(NEW.email,'')) !~ '^[^@[:space:]]+@ingenieria\.usac\.edu\.gt$' THEN
    RAISE EXCEPTION 'El registro requiere correo @ingenieria.usac.edu.gt';
  END IF;
  RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS prep_validate_signup_domain_trigger ON auth.users;
CREATE TRIGGER prep_validate_signup_domain_trigger
BEFORE INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.prep_validate_signup_domain();

CREATE OR REPLACE FUNCTION public.prep_create_pending_profile()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE
  v_name text := trim(coalesce(NEW.raw_user_meta_data->>'full_name',''));
  v_student text := trim(coalesce(NEW.raw_user_meta_data->>'student_id',''));
  v_career text := coalesce(NEW.raw_user_meta_data->>'career_code','');
BEGIN
  IF length(v_name) < 5 OR length(v_student) < 1 OR length(v_student) > 32
     OR v_career NOT IN ('IE','IEL','IME') THEN
    RAISE EXCEPTION 'Datos de inscripción incompletos o inválidos';
  END IF;
  INSERT INTO public.profiles(id,full_name,role,student_id,career_code,status)
  VALUES (NEW.id,v_name,'estudiante',v_student,v_career,'pendiente')
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS prep_create_pending_profile_trigger ON auth.users;
CREATE TRIGGER prep_create_pending_profile_trigger
AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.prep_create_pending_profile();

CREATE OR REPLACE FUNCTION public.prep_is_admin()
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
 SELECT EXISTS (SELECT 1 FROM public.profiles
 WHERE id=auth.uid() AND role='administrador' AND status='activo');
$$;

CREATE OR REPLACE FUNCTION public.prep_pending_registrations()
RETURNS TABLE(id uuid,full_name text,student_id text,career_code text,email text,created_at timestamptz)
LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = '' AS $$
BEGIN
 IF NOT public.prep_is_admin() THEN RAISE EXCEPTION 'Acceso denegado'; END IF;
 RETURN QUERY
 SELECT p.id,p.full_name,p.student_id,p.career_code,u.email::text,p.created_at
 FROM public.profiles p JOIN auth.users u ON u.id=p.id
 WHERE p.status='pendiente' AND p.role='estudiante'
 ORDER BY p.created_at ASC LIMIT 100;
END; $$;

CREATE OR REPLACE FUNCTION public.prep_decide_registration(p_profile_id uuid,p_approve boolean)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
 IF NOT public.prep_is_admin() THEN RAISE EXCEPTION 'Acceso denegado'; END IF;
 UPDATE public.profiles SET status=CASE WHEN p_approve THEN 'activo' ELSE 'rechazado' END
 WHERE id=p_profile_id AND role='estudiante' AND status='pendiente';
 RETURN FOUND;
END; $$;

REVOKE ALL ON FUNCTION public.prep_is_admin() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.prep_pending_registrations() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.prep_decide_registration(uuid,boolean) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.prep_is_admin() TO authenticated;
GRANT EXECUTE ON FUNCTION public.prep_pending_registrations() TO authenticated;
GRANT EXECUTE ON FUNCTION public.prep_decide_registration(uuid,boolean) TO authenticated;
COMMIT;
