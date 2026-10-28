-- PREP-EIME 1.8.0: integridad de calificaciones administrativas.
-- Requiere funciones current_user_can_publish_grades y publish_attempt_grades ya instaladas.
BEGIN;
CREATE OR REPLACE FUNCTION public.guard_administrative_attempt_grade()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
  IF NEW.grading_mode = 'administrativa' THEN
    IF NEW.grading_status IS DISTINCT FROM 'publicado' AND NEW.score IS NOT NULL THEN
      RAISE EXCEPTION 'No se puede guardar una nota administrativa antes de publicar';
    END IF;
    IF NEW.grading_status = 'publicado' AND
       (NEW.score IS NULL OR NEW.published_at IS NULL OR NEW.published_by IS NULL) THEN
      RAISE EXCEPTION 'La publicación requiere nota, fecha y administrador';
    END IF;
  END IF;
  IF auth.role() = 'authenticated' AND NOT public.current_user_can_publish_grades() THEN
    IF TG_OP = 'INSERT' THEN
      IF NEW.grading_status = 'publicado' THEN
        RAISE EXCEPTION 'No autorizado para publicar';
      END IF;
    ELSIF NEW.grading_mode IS DISTINCT FROM OLD.grading_mode
       OR NEW.grading_status IS DISTINCT FROM OLD.grading_status
       OR NEW.score IS DISTINCT FROM OLD.score
       OR NEW.published_at IS DISTINCT FROM OLD.published_at
       OR NEW.published_by IS DISTINCT FROM OLD.published_by THEN
      RAISE EXCEPTION 'No autorizado para cambiar campos de evaluación';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS trg_guard_administrative_attempt_grade ON public.attempts;
CREATE TRIGGER trg_guard_administrative_attempt_grade BEFORE INSERT OR UPDATE ON public.attempts
FOR EACH ROW EXECUTE FUNCTION public.guard_administrative_attempt_grade();

CREATE OR REPLACE FUNCTION public.guard_finalized_answer_membership()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE v_status text;
BEGIN
  IF auth.role() IS DISTINCT FROM 'authenticated' THEN RETURN COALESCE(NEW, OLD); END IF;
  SELECT a.status INTO v_status FROM public.attempts a
  WHERE a.id = COALESCE(NEW.attempt_id, OLD.attempt_id) FOR UPDATE;
  IF v_status = 'finalizado' THEN
    RAISE EXCEPTION 'No se pueden agregar o eliminar respuestas de un simulacro finalizado';
  END IF;
  RETURN COALESCE(NEW, OLD);
END;
$$;
DROP TRIGGER IF EXISTS trg_guard_finalized_answer_membership ON public.attempt_answers;
CREATE TRIGGER trg_guard_finalized_answer_membership BEFORE INSERT OR DELETE ON public.attempt_answers
FOR EACH ROW EXECUTE FUNCTION public.guard_finalized_answer_membership();

CREATE OR REPLACE FUNCTION public.guard_administrative_answer_scores()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE v_mode text;
BEGIN
  SELECT a.grading_mode INTO v_mode FROM public.attempts a WHERE a.id = NEW.attempt_id;
  IF v_mode = 'administrativa' AND
     (NEW.score IS NOT NULL OR NEW.review_score IS NOT NULL
      OR NEW.auto_score IS NOT NULL OR NEW.self_score IS NOT NULL
      OR NEW.feedback IS NOT NULL) THEN
    RAISE EXCEPTION 'Las notas administrativas deben permanecer en tablas de rúbricas';
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS trg_guard_administrative_answer_scores ON public.attempt_answers;
CREATE TRIGGER trg_guard_administrative_answer_scores BEFORE INSERT OR UPDATE ON public.attempt_answers
FOR EACH ROW EXECUTE FUNCTION public.guard_administrative_answer_scores();
REVOKE ALL ON FUNCTION public.guard_administrative_attempt_grade() FROM PUBLIC, anon, authenticated;
REVOKE ALL ON FUNCTION public.guard_finalized_answer_membership() FROM PUBLIC, anon, authenticated;
REVOKE ALL ON FUNCTION public.guard_administrative_answer_scores() FROM PUBLIC, anon, authenticated;
COMMIT;
