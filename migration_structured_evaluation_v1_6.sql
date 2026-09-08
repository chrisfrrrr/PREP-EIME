-- ============================================================
-- PREP-EIME v1.6 | Evaluación estructurada
-- Agrega respuestas autocalificables, rúbricas y revisión docente.
-- Idempotente: puede ejecutarse una sola vez o repetirse sin destruir datos.
-- ============================================================

alter table public.questions
  add column if not exists evaluation_mode text not null default 'autoevaluacion',
  add column if not exists answer_config jsonb not null default '{}'::jsonb,
  add column if not exists rubric jsonb not null default '[]'::jsonb,
  add column if not exists weight numeric(8,3) not null default 1;

alter table public.attempt_answers
  add column if not exists auto_score numeric(5,2),
  add column if not exists review_score numeric(5,2),
  add column if not exists reviewed_by uuid references public.profiles(id),
  add column if not exists reviewed_at timestamptz;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'questions_evaluation_mode_check'
  ) then
    alter table public.questions
      add constraint questions_evaluation_mode_check
      check (evaluation_mode in ('autocalificable','autoevaluacion','rubrica'));
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname = 'questions_weight_check'
  ) then
    alter table public.questions
      add constraint questions_weight_check
      check (weight > 0);
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname = 'attempt_answers_auto_score_check'
  ) then
    alter table public.attempt_answers
      add constraint attempt_answers_auto_score_check
      check (auto_score is null or (auto_score >= 0 and auto_score <= 100));
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname = 'attempt_answers_review_score_check'
  ) then
    alter table public.attempt_answers
      add constraint attempt_answers_review_score_check
      check (review_score is null or (review_score >= 0 and review_score <= 100));
  end if;
end $$;

-- Personal académico puede actualizar respuestas para revisión docente.
drop policy if exists "Staff update attempt answers" on public.attempt_answers;
create policy "Staff update attempt answers"
on public.attempt_answers for update to authenticated
using (public.current_user_is_staff())
with check (public.current_user_is_staff());

create index if not exists idx_questions_evaluation_mode
  on public.questions(evaluation_mode);

create index if not exists idx_attempt_answers_reviewed_by
  on public.attempt_answers(reviewed_by);

-- Migración de preguntas existentes:
-- se conservan como autoevaluación guiada para no asumir respuestas correctas.
update public.questions
set evaluation_mode = 'autoevaluacion'
where evaluation_mode is null;
