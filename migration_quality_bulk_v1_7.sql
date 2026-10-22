-- PREP-EIME v1.7: revisión verificable y transición masiva controlada
create table if not exists public.question_quality_reviews (
  question_id uuid primary key references public.questions(id) on delete cascade,
  reviewer_id uuid not null references public.profiles(id),
  reviewed_at timestamptz not null default now(),
  clarity boolean not null,
  topic_alignment boolean not null,
  technical_accuracy boolean not null,
  answer_quality boolean not null,
  evaluation_quality boolean not null,
  notes text,
  approved_for_publication boolean generated always as
    (clarity and topic_alignment and technical_accuracy and answer_quality and evaluation_quality) stored
);
alter table public.question_quality_reviews enable row level security;
drop policy if exists "Staff read quality reviews" on public.question_quality_reviews;
create policy "Staff read quality reviews" on public.question_quality_reviews
for select to authenticated using (public.current_user_is_staff());
drop policy if exists "Staff create quality reviews" on public.question_quality_reviews;
create policy "Staff create quality reviews" on public.question_quality_reviews
for insert to authenticated
with check (public.current_user_is_staff() and reviewer_id=auth.uid());
drop policy if exists "Staff update own quality reviews" on public.question_quality_reviews;
create policy "Staff update own quality reviews" on public.question_quality_reviews
for update to authenticated
using (public.current_user_is_staff() and (reviewer_id=auth.uid() or public.current_user_role() in ('coordinador','administrador')))
with check (public.current_user_is_staff() and reviewer_id=auth.uid());

-- Garantía del lado de la base: nadie puede publicar una pregunta sin revisión positiva.
create or replace function public.enforce_question_quality_on_publish()
returns trigger language plpgsql security definer set search_path=public as $$
begin
  if new.status='publicado' and (tg_op='INSERT' or old.status is distinct from 'publicado') then
    if not exists (
      select 1 from public.question_quality_reviews r
      where r.question_id=new.id and r.approved_for_publication=true
    ) then
      raise exception 'Pregunta % sin revisión académica positiva',new.id;
    end if;
  end if;
  return new;
end; $$;
drop trigger if exists trg_enforce_question_quality on public.questions;
create trigger trg_enforce_question_quality
before insert or update of status on public.questions
for each row execute function public.enforce_question_quality_on_publish();

-- Cambios de contenido invalidan la revisión previa (salvo transición editorial).
create or replace function public.invalidate_question_quality()
returns trigger language plpgsql security definer set search_path=public as $$
begin
  if (old.question_text,old.expected_answer,old.course_code,old.topic_id,
      old.answer_config,old.rubric,old.evaluation_mode,old.weight,old.question_type)
     is distinct from
     (new.question_text,new.expected_answer,new.course_code,new.topic_id,
      new.answer_config,new.rubric,new.evaluation_mode,new.weight,new.question_type) then
    if old.status='publicado' then
      raise exception 'Despublica la pregunta antes de editar su contenido técnico';
    end if;
    delete from public.question_quality_reviews where question_id=new.id;
  end if;
  return new;
end; $$;
drop trigger if exists trg_invalidate_question_quality on public.questions;
create trigger trg_invalidate_question_quality
after update on public.questions for each row execute function public.invalidate_question_quality();

-- Transiciones por lotes. No omite las etapas de revisión ni autoriza a docentes a publicar.
create or replace function public.bulk_transition_reviewed_questions(
  p_question_ids uuid[], p_target text
) returns table(question_id uuid, outcome text)
language plpgsql security invoker set search_path=public as $$
declare v_id uuid; v_current text; v_role public.user_role; v_allowed boolean;
begin
  v_role:=public.current_user_role();
  if v_role not in ('coordinador','administrador') then
    raise exception 'Se requiere rol coordinador o administrador';
  end if;
  if p_target not in ('en_revision','aprobado','publicado') then
    raise exception 'Transición no permitida';
  end if;
  if coalesce(array_length(p_question_ids,1),0)>100 then
    raise exception 'Máximo 100 preguntas por operación';
  end if;
  foreach v_id in array p_question_ids loop
    select q.status::text into v_current from public.questions q where q.id=v_id for update;
    if v_current is null then
      question_id:=v_id; outcome:='No encontrada o sin permiso'; return next;
    else
      v_allowed:=(v_current='borrador' and p_target='en_revision')
        or (v_current='en_revision' and p_target='aprobado')
        or (v_current='aprobado' and p_target='publicado');
      if not v_allowed then
        question_id:=v_id; outcome:='Transición no válida desde '||v_current; return next;
      elsif not exists (
        select 1 from public.question_quality_reviews r
        where r.question_id=v_id and r.approved_for_publication=true
      ) then
        question_id:=v_id; outcome:='Falta revisión positiva'; return next;
      else
        update public.questions set status=p_target::public.content_status where id=v_id;
        question_id:=v_id; outcome:='Actualizada a '||p_target; return next;
      end if;
    end if;
  end loop;
end; $$;
revoke all on function public.bulk_transition_reviewed_questions(uuid[],text) from public;
grant execute on function public.bulk_transition_reviewed_questions(uuid[],text) to authenticated;
