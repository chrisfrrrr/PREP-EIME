
insert into public.careers(code,name) values
('IME','Ingeniería Mecánica Eléctrica'),
('IE','Ingeniería Eléctrica'),
('IEL','Ingeniería Electrónica')
on conflict do nothing;

insert into public.cohorts(code,name,starts_on,ends_on,active) values
('EGP-2026-II','Propedéutico EGP 2026-II','2026-09-01','2026-12-15',true)
on conflict do nothing;

insert into public.egp_areas(name) values
('Circuitos eléctricos'),
('Electromagnetismo'),
('Electrónica'),
('Instrumentación'),
('Conversión de energía'),
('Máquinas eléctricas'),
('Sistemas de control'),
('Automatización'),
('Sistemas eléctricos de potencia'),
('Instalaciones eléctricas'),
('Comunicaciones y telecomunicaciones'),
('Ingeniería mecánica'),
('Energía térmica'),
('Diseño y mantenimiento')
on conflict do nothing;

-- Los cursos y sus vínculos finales se completarán después de validar
-- la matriz maestra contra los programas oficiales.
