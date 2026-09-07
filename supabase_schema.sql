
-- PREP-EIME v1.0
-- Esquema base para Supabase/PostgreSQL

create extension if not exists "pgcrypto";

create type public.user_role as enum ('estudiante','docente','coordinador','administrador');
create type public.content_status as enum ('borrador','en_revision','aprobado','publicado','archivado');

create table public.careers (
  code text primary key,
  name text not null unique,
  active boolean not null default true
);

create table public.cohorts (
  code text primary key,
  name text not null,
  starts_on date,
  ends_on date,
  active boolean not null default true
);

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null,
  role public.user_role not null default 'estudiante',
  student_id text,
  career_code text references public.careers(code),
  cohort_code text references public.cohorts(code),
  status text not null default 'activo',
  created_at timestamptz not null default now()
);

create table public.egp_areas (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  description text,
  active boolean not null default true
);

create table public.courses (
  code text primary key,
  name text not null,
  semester integer,
  area_id uuid references public.egp_areas(id),
  active boolean not null default true
);

create table public.career_courses (
  career_code text references public.careers(code) on delete cascade,
  course_code text references public.courses(code) on delete cascade,
  is_egp_required boolean not null default true,
  primary key (career_code, course_code)
);

create table public.course_programs (
  id uuid primary key default gen_random_uuid(),
  course_code text not null references public.courses(code) on delete cascade,
  version_label text not null,
  effective_year integer,
  source_note text,
  status public.content_status not null default 'borrador',
  created_by uuid references public.profiles(id),
  created_at timestamptz not null default now(),
  unique(course_code, version_label)
);

create table public.topics (
  id uuid primary key default gen_random_uuid(),
  course_program_id uuid not null references public.course_programs(id) on delete cascade,
  parent_id uuid references public.topics(id) on delete cascade,
  title text not null,
  sort_order integer not null default 0,
  body_md text,
  status public.content_status not null default 'borrador'
);

create table public.resources (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid references public.topics(id) on delete set null,
  title text not null,
  resource_type text not null,
  storage_path text,
  external_url text,
  status public.content_status not null default 'borrador',
  created_by uuid references public.profiles(id),
  created_at timestamptz not null default now()
);

create table public.questions (
  id uuid primary key default gen_random_uuid(),
  area_id uuid references public.egp_areas(id),
  course_code text references public.courses(code),
  topic_id uuid references public.topics(id),
  question_text text not null,
  expected_answer text,
  difficulty smallint check (difficulty between 1 and 5),
  competency text,
  question_type text,
  status public.content_status not null default 'borrador',
  created_by uuid references public.profiles(id),
  created_at timestamptz not null default now()
);

create table public.question_careers (
  question_id uuid references public.questions(id) on delete cascade,
  career_code text references public.careers(code) on delete cascade,
  primary key (question_id, career_code)
);

create table public.attempts (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,
  attempt_type text not null,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  score numeric(5,2)
);

create table public.attempt_answers (
  id uuid primary key default gen_random_uuid(),
  attempt_id uuid not null references public.attempts(id) on delete cascade,
  question_id uuid not null references public.questions(id),
  answer_text text,
  score numeric(5,2),
  feedback text
);

create table public.activity_log (
  id bigint generated always as identity primary key,
  user_id uuid references public.profiles(id) on delete set null,
  event_type text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- RLS
alter table public.profiles enable row level security;
alter table public.careers enable row level security;
alter table public.cohorts enable row level security;
alter table public.egp_areas enable row level security;
alter table public.courses enable row level security;
alter table public.career_courses enable row level security;
alter table public.course_programs enable row level security;
alter table public.topics enable row level security;
alter table public.resources enable row level security;
alter table public.questions enable row level security;
alter table public.question_careers enable row level security;
alter table public.attempts enable row level security;
alter table public.attempt_answers enable row level security;
alter table public.activity_log enable row level security;

-- Lectura general de catálogos para usuarios autenticados
create policy "Authenticated read careers"
on public.careers for select to authenticated using (true);

create policy "Authenticated read cohorts"
on public.cohorts for select to authenticated using (true);

create policy "Authenticated read areas"
on public.egp_areas for select to authenticated using (true);

create policy "Authenticated read courses"
on public.courses for select to authenticated using (true);

create policy "Authenticated read career_courses"
on public.career_courses for select to authenticated using (true);

-- Cada usuario puede leer su propio perfil
create policy "Read own profile"
on public.profiles for select to authenticated
using (id = auth.uid());

-- Estudiantes: solo sus intentos
create policy "Students read own attempts"
on public.attempts for select to authenticated
using (student_id = auth.uid());

create policy "Students insert own attempts"
on public.attempts for insert to authenticated
with check (student_id = auth.uid());

create policy "Students read own answers"
on public.attempt_answers for select to authenticated
using (
  exists (
    select 1 from public.attempts a
    where a.id = attempt_id and a.student_id = auth.uid()
  )
);

-- Contenido publicado visible a autenticados
create policy "Read published programs"
on public.course_programs for select to authenticated
using (status = 'publicado');

create policy "Read published topics"
on public.topics for select to authenticated
using (status = 'publicado');

create policy "Read published resources"
on public.resources for select to authenticated
using (status = 'publicado');

create policy "Read published questions"
on public.questions for select to authenticated
using (status = 'publicado');

create policy "Read question careers"
on public.question_careers for select to authenticated
using (true);

-- Nota:
-- Las políticas de escritura para docentes/coordinación/administración
-- se añadirán después de crear funciones helper de rol con SECURITY DEFINER.
