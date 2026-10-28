-- PREP-EIME v1.8.1 / Consolidación de publicación y rúbricas.
-- Requiere migraciones previas y función get_my_published_attempt_result.
-- Ejecutar en Supabase SQL Editor. No borra datos ni recalcula notas.
BEGIN;

-- Bloqueo definitivo de las evaluaciones una vez publicada la nota.
CREATE OR REPLACE FUNCTION public.guard_published_rubric_mutations()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE
  v_attempt_id uuid;
  v_status text;
BEGIN
  IF TG_TABLE_NAME = 'answer_rubric_evaluations' THEN
    IF TG_OP = 'DELETE' THEN
      SELECT aa.attempt_id INTO v_attempt_id
      FROM public.attempt_answers aa WHERE aa.id = OLD.attempt_answer_id;
    ELSE
      SELECT aa.attempt_id INTO v_attempt_id
      FROM public.attempt_answers aa WHERE aa.id = NEW.attempt_answer_id;
    END IF;
  ELSE
    SELECT aa.attempt_id INTO v_attempt_id
    FROM public.answer_rubric_evaluations e
    JOIN public.attempt_answers aa ON aa.id = e.attempt_answer_id
    WHERE e.id = CASE WHEN TG_OP = 'DELETE' THEN OLD.evaluation_id ELSE NEW.evaluation_id END;
  END IF;

  SELECT a.grading_status INTO v_status
  FROM public.attempts a WHERE a.id = v_attempt_id FOR UPDATE;

  IF v_status = 'publicado' THEN
    RAISE EXCEPTION 'Las rúbricas de un simulacro publicado son inmutables';
  END IF;
  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_guard_published_evaluation ON public.answer_rubric_evaluations;
CREATE TRIGGER trg_guard_published_evaluation
BEFORE INSERT OR UPDATE OR DELETE ON public.answer_rubric_evaluations
FOR EACH ROW EXECUTE FUNCTION public.guard_published_rubric_mutations();

DROP TRIGGER IF EXISTS trg_guard_published_criteria ON public.answer_criterion_scores;
CREATE TRIGGER trg_guard_published_criteria
BEFORE INSERT OR UPDATE OR DELETE ON public.answer_criterion_scores
FOR EACH ROW EXECUTE FUNCTION public.guard_published_rubric_mutations();

-- La nota y los metadatos de publicación quedan congelados.
CREATE OR REPLACE FUNCTION public.guard_published_attempt_result()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
  IF OLD.grading_mode = 'administrativa' AND OLD.grading_status = 'publicado'
     AND (NEW.score IS DISTINCT FROM OLD.score
          OR NEW.grading_status IS DISTINCT FROM OLD.grading_status
          OR NEW.published_at IS DISTINCT FROM OLD.published_at
          OR NEW.published_by IS DISTINCT FROM OLD.published_by
          OR NEW.grading_mode IS DISTINCT FROM OLD.grading_mode) THEN
    RAISE EXCEPTION 'No se puede modificar un resultado oficialmente publicado';
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS trg_guard_published_attempt_result ON public.attempts;
CREATE TRIGGER trg_guard_published_attempt_result
BEFORE UPDATE ON public.attempts
FOR EACH ROW EXECUTE FUNCTION public.guard_published_attempt_result();

-- Lectura por estudiante exclusivamente de su intento publicado.
CREATE OR REPLACE FUNCTION public.get_my_published_rubric_details(p_attempt_id uuid)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE v_student_id uuid; v_mode text; v_status text; v_published_at timestamptz;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'Se requiere autenticación';
  END IF;
  SELECT a.student_id,a.grading_mode,a.grading_status,a.published_at
  INTO v_student_id,v_mode,v_status,v_published_at
  FROM public.attempts a WHERE a.id=p_attempt_id;

  IF v_student_id IS DISTINCT FROM auth.uid() THEN
    RAISE EXCEPTION 'No se encontró un simulacro propio';
  END IF;
  IF v_mode IS DISTINCT FROM 'administrativa'
     OR v_status IS DISTINCT FROM 'publicado'
     OR v_published_at IS NULL THEN
    RETURN '[]'::jsonb;
  END IF;
  RETURN COALESCE((
    SELECT jsonb_agg(jsonb_build_object(
      'answer_id',aa.id,
      'rubric_name',r.name,
      'answer_score',COALESCE((
         SELECT SUM(cs2.awarded_points) FROM public.answer_criterion_scores cs2
         WHERE cs2.evaluation_id=e.id
      ),0),
      'criteria',COALESCE((
         SELECT jsonb_agg(jsonb_build_object(
           'criterion_name',gc.name,
           'performance_level',cs.performance_level,
           'awarded_points',cs.awarded_points,
           'max_points',gc.max_points
         ) ORDER BY cs.criterion_order)
         FROM public.answer_criterion_scores cs
         JOIN public.grading_criteria gc
           ON gc.rubric_id=e.rubric_id AND gc.criterion_order=cs.criterion_order
         WHERE cs.evaluation_id=e.id
      ),'[]'::jsonb)
    ) ORDER BY aa.id)
    FROM public.attempt_answers aa
    JOIN public.answer_rubric_evaluations e ON e.attempt_answer_id=aa.id
    JOIN public.grading_rubrics r ON r.id=e.rubric_id
    WHERE aa.attempt_id=p_attempt_id AND e.status='completa'
  ),'[]'::jsonb);
END;
$$;

REVOKE ALL ON FUNCTION public.guard_published_rubric_mutations() FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION public.guard_published_attempt_result() FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION public.get_my_published_rubric_details(uuid) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.get_my_published_rubric_details(uuid) TO authenticated;
COMMIT;
