-- PREP-EIME v1.8.0 / Etapa 130: integridad de respuestas tras finalizar.
-- Ejecutar en Supabase SQL Editor. No altera respuestas existentes.
-- No activa publicación ni modifica los permisos SELECT.
CREATE OR REPLACE FUNCTION public.guard_finalized_attempt_answer_changes()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE
  v_status text;
  v_role text;
BEGIN
  -- Solo aplica a ediciones desde sesiones autenticadas; las operaciones
  -- de mantenimiento realizadas por service_role no se bloquean.
  IF auth.role() IS DISTINCT FROM 'authenticated' THEN
    RETURN NEW;
  END IF;
  SELECT a.status INTO v_status
  FROM public.attempts a WHERE a.id = OLD.attempt_id;
  IF v_status = 'finalizado' AND
     (NEW.answer_text IS DISTINCT FROM OLD.answer_text OR
      NEW.answered_at IS DISTINCT FROM OLD.answered_at OR
      NEW.attempt_id IS DISTINCT FROM OLD.attempt_id OR
      NEW.question_id IS DISTINCT FROM OLD.question_id) THEN
    SELECT p.role INTO v_role FROM public.profiles p WHERE p.id = auth.uid();
    IF v_role IS DISTINCT FROM 'administrador' THEN
      RAISE EXCEPTION 'Las respuestas de un simulacro finalizado no pueden modificarse.';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS trg_guard_finalized_attempt_answer_changes ON public.attempt_answers;
CREATE TRIGGER trg_guard_finalized_attempt_answer_changes
BEFORE UPDATE ON public.attempt_answers
FOR EACH ROW EXECUTE FUNCTION public.guard_finalized_attempt_answer_changes();
REVOKE ALL ON FUNCTION public.guard_finalized_attempt_answer_changes() FROM PUBLIC, anon, authenticated;
