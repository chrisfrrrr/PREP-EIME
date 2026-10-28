-- PREP-EIME 1.8.0 — Paso de consulta segura (sin publicación).
-- Crear esta RPC antes de probar la nueva vista estudiantil.
CREATE OR REPLACE FUNCTION public.get_my_published_attempt_result(p_attempt_id uuid)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_row record;
BEGIN
    IF auth.uid() IS NULL THEN
        RAISE EXCEPTION 'Se requiere una sesión autenticada.';
    END IF;
    SELECT a.student_id, a.grading_mode, a.grading_status,
           a.score, a.published_at
      INTO v_row
      FROM public.attempts a
     WHERE a.id = p_attempt_id;
    IF NOT FOUND OR v_row.student_id IS DISTINCT FROM auth.uid() THEN
        RAISE EXCEPTION 'No se encontró un simulacro propio.';
    END IF;
    IF v_row.grading_mode IS DISTINCT FROM 'administrativa' THEN
        RETURN jsonb_build_object('published', false, 'historical', true);
    END IF;
    IF v_row.grading_status = 'publicado'
       AND v_row.published_at IS NOT NULL
       AND v_row.score IS NOT NULL THEN
        RETURN jsonb_build_object('published', true,
            'score', v_row.score, 'published_at', v_row.published_at);
    END IF;
    RETURN jsonb_build_object('published', false);
END;
$$;
REVOKE ALL ON FUNCTION public.get_my_published_attempt_result(uuid)
FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.get_my_published_attempt_result(uuid)
TO authenticated;
