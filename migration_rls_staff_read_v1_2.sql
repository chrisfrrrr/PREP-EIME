-- PREP-EIME v1.2
-- Permite que docentes, coordinadores y administradores revisen contenido no publicado.
-- Los estudiantes conservan acceso únicamente al contenido publicado.

create or replace function public.current_user_is_staff()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.status = 'activo'
      and p.role in ('docente','coordinador','administrador')
  );
$$;

revoke all on function public.current_user_is_staff() from public;
grant execute on function public.current_user_is_staff() to authenticated;

-- Lectura de perfiles para el propio usuario ya existe. No se modifica aquí.

create policy "Staff read all programs"
on public.course_programs for select to authenticated
using (public.current_user_is_staff());

create policy "Staff read all topics"
on public.topics for select to authenticated
using (public.current_user_is_staff());

create policy "Staff read all resources"
on public.resources for select to authenticated
using (public.current_user_is_staff());

create policy "Staff read all questions"
on public.questions for select to authenticated
using (public.current_user_is_staff());
