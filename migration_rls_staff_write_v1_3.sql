-- PREP-EIME v1.3
-- Escritura académica controlada por rol.
-- Docente: borrador / en_revision.
-- Coordinador y administrador: pueden aprobar y publicar.
-- Administrador: además puede eliminar programas/temas si fuera necesario.

create or replace function public.current_user_role()
returns public.user_role
language sql
stable
security definer
set search_path = public
as $$
  select p.role
  from public.profiles p
  where p.id = auth.uid()
    and p.status = 'activo'
  limit 1;
$$;

revoke all on function public.current_user_role() from public;
grant execute on function public.current_user_role() to authenticated;

-- PROGRAMAS --------------------------------------------------------
drop policy if exists "Staff insert programs" on public.course_programs;
create policy "Staff insert programs"
on public.course_programs for insert to authenticated
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
    and created_by = auth.uid()
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Staff update programs" on public.course_programs;
create policy "Staff update programs"
on public.course_programs for update to authenticated
using (public.current_user_is_staff())
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Admin delete programs" on public.course_programs;
create policy "Admin delete programs"
on public.course_programs for delete to authenticated
using (public.current_user_role() = 'administrador');

-- TEMAS / UNIDADES -------------------------------------------------
drop policy if exists "Staff insert topics" on public.topics;
create policy "Staff insert topics"
on public.topics for insert to authenticated
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Staff update topics" on public.topics;
create policy "Staff update topics"
on public.topics for update to authenticated
using (public.current_user_is_staff())
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Admin delete topics" on public.topics;
create policy "Admin delete topics"
on public.topics for delete to authenticated
using (public.current_user_role() = 'administrador');

-- RECURSOS: dejamos preparada la escritura para la siguiente etapa.
drop policy if exists "Staff insert resources" on public.resources;
create policy "Staff insert resources"
on public.resources for insert to authenticated
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
    and created_by = auth.uid()
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Staff update resources" on public.resources;
create policy "Staff update resources"
on public.resources for update to authenticated
using (public.current_user_is_staff())
with check (
  (
    public.current_user_role() = 'docente'
    and status in ('borrador','en_revision')
  )
  or public.current_user_role() in ('coordinador','administrador')
);

drop policy if exists "Admin delete resources" on public.resources;
create policy "Admin delete resources"
on public.resources for delete to authenticated
using (public.current_user_role() = 'administrador');
