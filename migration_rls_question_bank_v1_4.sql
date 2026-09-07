-- =========================================================
-- PREP-EIME v1.4 | Banco de Preguntas EGP
-- Habilita lectura completa para personal académico y escritura
-- controlada por rol sobre questions y question_careers.
-- =========================================================

-- Lectura de preguntas no publicadas para personal académico
drop policy if exists "Staff read questions" on public.questions;
create policy "Staff read questions"
on public.questions for select to authenticated
using (public.current_user_is_staff());

-- INSERT
drop policy if exists "Staff insert questions" on public.questions;
create policy "Staff insert questions"
on public.questions for insert to authenticated
with check (
    (
        public.current_user_role() = 'docente'
        and status in ('borrador','en_revision')
        and created_by = auth.uid()
    )
    or public.current_user_role() in ('coordinador','administrador')
);

-- UPDATE
drop policy if exists "Staff update questions" on public.questions;
create policy "Staff update questions"
on public.questions for update to authenticated
using (public.current_user_is_staff())
with check (
    (
        public.current_user_role() = 'docente'
        and status in ('borrador','en_revision')
    )
    or public.current_user_role() in ('coordinador','administrador')
);

-- DELETE solo administrador
drop policy if exists "Admin delete questions" on public.questions;
create policy "Admin delete questions"
on public.questions for delete to authenticated
using (public.current_user_role() = 'administrador');

-- Relaciones pregunta ↔ carrera
drop policy if exists "Staff insert question careers" on public.question_careers;
create policy "Staff insert question careers"
on public.question_careers for insert to authenticated
with check (public.current_user_is_staff());

drop policy if exists "Staff delete question careers" on public.question_careers;
create policy "Staff delete question careers"
on public.question_careers for delete to authenticated
using (public.current_user_is_staff());

-- Índices útiles para filtros del banco
create index if not exists idx_questions_course_code on public.questions(course_code);
create index if not exists idx_questions_topic_id on public.questions(topic_id);
create index if not exists idx_questions_status on public.questions(status);
create index if not exists idx_questions_difficulty on public.questions(difficulty);
create index if not exists idx_question_careers_career_code on public.question_careers(career_code);
