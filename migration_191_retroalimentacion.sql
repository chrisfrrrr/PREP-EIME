-- PREP-EIME v1.9.1. Ejecutar UNA VEZ en Supabase SQL Editor.
BEGIN;
CREATE TABLE IF NOT EXISTS public.answer_feedback (
 attempt_answer_id uuid PRIMARY KEY REFERENCES public.attempt_answers(id) ON DELETE CASCADE,
 observation text NOT NULL DEFAULT '',
 recommendation text NOT NULL DEFAULT '',
 updated_by uuid NOT NULL REFERENCES auth.users(id),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT feedback_observation_length CHECK (length(observation)<=4000),
 CONSTRAINT feedback_recommendation_length CHECK (length(recommendation)<=4000)
);
ALTER TABLE public.answer_feedback ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.answer_feedback FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.answer_feedback TO authenticated;
DROP POLICY IF EXISTS feedback_admin_read ON public.answer_feedback;
CREATE POLICY feedback_admin_read ON public.answer_feedback FOR SELECT TO authenticated
 USING (public.current_user_can_grade());

CREATE OR REPLACE FUNCTION public.save_answer_feedback(
 p_answer_id uuid, p_observation text, p_recommendation text
) RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE v_status text; v_mode text;
BEGIN
 IF auth.uid() IS NULL OR NOT public.current_user_can_grade() THEN
  RAISE EXCEPTION 'No autorizado para evaluar';
 END IF;
 SELECT a.grading_status,a.grading_mode INTO v_status,v_mode
 FROM public.attempt_answers aa JOIN public.attempts a ON a.id=aa.attempt_id
 WHERE aa.id=p_answer_id FOR UPDATE OF a;
 IF NOT FOUND OR v_mode IS DISTINCT FROM 'administrativa' THEN
  RAISE EXCEPTION 'Respuesta administrativa no encontrada';
 END IF;
 IF v_status='publicado' THEN
  RAISE EXCEPTION 'La evaluación ya está publicada y no se puede modificar';
 END IF;
 INSERT INTO public.answer_feedback(attempt_answer_id,observation,recommendation,updated_by,updated_at)
 VALUES (p_answer_id,COALESCE(p_observation,''),COALESCE(p_recommendation,''),auth.uid(),now())
 ON CONFLICT (attempt_answer_id) DO UPDATE SET
 observation=EXCLUDED.observation,recommendation=EXCLUDED.recommendation,
 updated_by=EXCLUDED.updated_by,updated_at=now();
 RETURN true;
END;
$$;

CREATE OR REPLACE FUNCTION public.get_my_published_feedback(p_attempt_id uuid)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE v_student uuid; v_mode text; v_status text; v_published timestamptz;
BEGIN
 IF auth.uid() IS NULL THEN RAISE EXCEPTION 'Se requiere autenticación'; END IF;
 SELECT student_id,grading_mode,grading_status,published_at
 INTO v_student,v_mode,v_status,v_published FROM public.attempts WHERE id=p_attempt_id;
 IF v_student IS DISTINCT FROM auth.uid() THEN
  RAISE EXCEPTION 'Simulacro propio no encontrado';
 END IF;
 IF v_mode IS DISTINCT FROM 'administrativa' OR v_status IS DISTINCT FROM 'publicado'
    OR v_published IS NULL THEN RETURN '[]'::jsonb; END IF;
 RETURN COALESCE((SELECT jsonb_agg(jsonb_build_object(
  'answer_id',aa.id,'observation',f.observation,'recommendation',f.recommendation
 ) ORDER BY aa.id)
 FROM public.attempt_answers aa JOIN public.answer_feedback f ON f.attempt_answer_id=aa.id
 WHERE aa.attempt_id=p_attempt_id),'[]'::jsonb);
END;
$$;
REVOKE ALL ON FUNCTION public.save_answer_feedback(uuid,text,text) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.save_answer_feedback(uuid,text,text) TO authenticated;
REVOKE ALL ON FUNCTION public.get_my_published_feedback(uuid) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.get_my_published_feedback(uuid) TO authenticated;
COMMIT;
