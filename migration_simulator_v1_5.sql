-- ============================================================
-- PREP-EIME v1.5 | Simulador EGP escrito
-- Amplía attempts / attempt_answers sin destruir datos previos.
-- ============================================================

alter table public.attempts
  add column if not exists career_code text references public.careers(code),
  add column if not exists status text not null default 'en_progreso',
  add column if not exists duration_minutes integer,
  add column if not exists question_count integer,
  add column if not exists metadata jsonb not null default '{}'::jsonb;

alter table public.attempt_answers
  add column if not exists self_score numeric(5,2),
  add column if not exists evaluation_status text not null default 'pendiente',
  add column if not exists answered_at timestamptz;

-- Índices
create index if not exists idx_attempts_student_started
  on public.attempts(student_id, started_at desc);

create index if not exists idx_attempts_status
  on public.attempts(status);

create index if not exists idx_attempt_answers_attempt
  on public.attempt_answers(attempt_id);

-- El estudiante puede actualizar sus propios intentos
drop policy if exists "Students update own attempts" on public.attempts;
create policy "Students update own attempts"
on public.attempts for update to authenticated
using (student_id = auth.uid())
with check (student_id = auth.uid());

-- El estudiante puede insertar respuestas de sus propios intentos
drop policy if exists "Students insert own answers" on public.attempt_answers;
create policy "Students insert own answers"
on public.attempt_answers for insert to authenticated
with check (
  exists (
    select 1
    from public.attempts a
    where a.id = attempt_id
      and a.student_id = auth.uid()
  )
);

-- El estudiante puede actualizar respuestas de sus propios intentos
drop policy if exists "Students update own answers" on public.attempt_answers;
create policy "Students update own answers"
on public.attempt_answers for update to authenticated
using (
  exists (
    select 1
    from public.attempts a
    where a.id = attempt_id
      and a.student_id = auth.uid()
  )
)
with check (
  exists (
    select 1
    from public.attempts a
    where a.id = attempt_id
      and a.student_id = auth.uid()
  )
);

-- Personal académico puede leer intentos y respuestas para seguimiento
drop policy if exists "Staff read attempts" on public.attempts;
create policy "Staff read attempts"
on public.attempts for select to authenticated
using (public.current_user_is_staff());

drop policy if exists "Staff read attempt answers" on public.attempt_answers;
create policy "Staff read attempt answers"
on public.attempt_answers for select to authenticated
using (public.current_user_is_staff());

-- Restricciones blandas de calidad
do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'attempts_status_check'
  ) then
    alter table public.attempts
      add constraint attempts_status_check
      check (status in ('en_progreso','finalizado','cancelado'));
  end if;

  if not exists (
    select 1
    from pg_constraint
    where conname = 'attempt_answers_evaluation_status_check'
  ) then
    alter table public.attempt_answers
      add constraint attempt_answers_evaluation_status_check
      check (evaluation_status in ('pendiente','autoevaluado','revisado'));
  end if;

  if not exists (
    select 1
    from pg_constraint
    where conname = 'attempt_answers_self_score_check'
  ) then
    alter table public.attempt_answers
      add constraint attempt_answers_self_score_check
      check (self_score is null or (self_score >= 0 and self_score <= 100));
  end if;
end $$;
