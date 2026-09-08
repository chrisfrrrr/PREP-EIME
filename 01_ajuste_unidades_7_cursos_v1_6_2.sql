-- ================================================================
-- PREP-EIME v1.6.2 | NORMALIZACIÓN DE UNIDADES DE 7 CURSOS
-- Corrige los cursos que en v1.6.1 no tenían topics.
-- No elimina datos existentes. Es idempotente mediante WHERE NOT EXISTS.
-- ================================================================
begin;

-- 0250 · Mecánica de Fluidos
-- Fuente de normalización: Programa USAC, Escuela de Ingeniería Civil, Área de Hidráulica, código 250
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Introducción a la Mecánica de Fluidos',1,'Definición de mecánica de fluidos; relación con otras disciplinas de ingeniería; dimensiones, unidades y factores de conversión.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Introducción a la Mecánica de Fluidos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Definición y propiedades de los fluidos',2,'Definición de fluido; densidad; peso específico; gravedad específica; volumen específico; viscosidad; ley de Newton de la viscosidad; módulo de elasticidad; tensión superficial; presión de vapor; gas perfecto; fluido ideal.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Definición y propiedades de los fluidos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Hidrostática',3,'Presión; ecuación fundamental de la hidrostática; presión atmosférica, absoluta y relativa; manometría; fuerzas sobre superficies planas y curvas sumergidas; empuje y estabilidad de cuerpos flotantes.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Hidrostática'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Cinemática de los fluidos',4,'Volumen de control; clasificación de flujos; flujo laminar y turbulento; estacionario y no estacionario; uniforme y variado; flujo uni, bi y tridimensional.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Cinemática de los fluidos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Dinámica de fluidos',5,'Líneas y tubos de corriente; conservación de la masa; ecuación de continuidad; conservación de la energía; ecuación general de energía; ecuación de Bernoulli; líneas piezométrica y de energía.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=5
      and t.title='Dinámica de fluidos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Cantidad de movimiento',6,'Introducción y derivación de la ecuación de cantidad de movimiento; aplicaciones de ingeniería.','borrador'
from public.course_programs cp
where cp.course_code='0250'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=6
      and t.title='Cantidad de movimiento'
  );

-- 0252 · Hidráulica
-- Fuente de normalización: Programa USAC de Hidráulica, código 252, estructura académica 2024
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Conceptos básicos de hidráulica',1,'Conceptos fundamentales para el análisis de flujo y conducción de líquidos.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Conceptos básicos de hidráulica'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Flujo en tuberías y conductos a presión',2,'Pérdidas por fricción; flujo laminar y turbulento; Hagen-Poiseuille; Colebrook; Darcy-Weisbach; Moody; Hazen-Williams; pérdidas localizadas; líneas piezométrica y de energía.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Flujo en tuberías y conductos a presión'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Flujo en sistemas de tuberías a presión',3,'Tuberías en serie, equivalentes, en paralelo y ramificadas; circuitos cerrados; método de Hardy-Cross.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Flujo en sistemas de tuberías a presión'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Sistemas de bombeo',4,'Cálculo y diseño de sistemas de bombeo; selección de bombas; fenómenos transitorios; golpe de ariete y accesorios de protección.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Sistemas de bombeo'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Flujo en canales abiertos',5,'Características y tipos de flujo; propiedades hidráulicas y geométricas; número de Froude; flujo uniforme; ecuación de Manning; energía específica y resalto hidráulico.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=5
      and t.title='Flujo en canales abiertos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Semejanza hidráulica',6,'Similitud geométrica, cinemática y dinámica; factores de escala; criterios de modelación hidráulica.','borrador'
from public.course_programs cp
where cp.course_code='0252'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=6
      and t.title='Semejanza hidráulica'
  );

-- 0258 · Máquinas Hidráulicas
-- Fuente de normalización: Programa oficial USAC, Escuela de Ingeniería Mecánica, código 258
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Generalidades de máquinas hidráulicas',1,'Conceptos fundamentales, clasificación y principios generales de las máquinas hidráulicas.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Generalidades de máquinas hidráulicas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Bombas',2,'Principios de operación, tipos, características, comportamiento y aplicaciones de bombas.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Bombas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Similitud y teoría de las máquinas hidráulicas',3,'Leyes de similitud, parámetros característicos y fundamentos de teoría de turbomáquinas.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Similitud y teoría de las máquinas hidráulicas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Cavitación',4,'Fundamentos, causas, efectos, identificación y prevención de cavitación.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Cavitación'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Selección de máquinas hidráulicas',5,'Criterios técnicos para determinar y seleccionar la máquina hidráulica adecuada a una aplicación.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=5
      and t.title='Selección de máquinas hidráulicas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Turbinas hidráulicas',6,'Clasificación, funcionamiento, características y aplicaciones de turbinas hidráulicas.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=6
      and t.title='Turbinas hidráulicas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Órganos principales de las turbinas',7,'Elementos principales de las turbinas hidráulicas y función de sus componentes.','borrador'
from public.course_programs cp
where cp.course_code='0258'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=7
      and t.title='Órganos principales de las turbinas'
  );

-- 0390 · Termodinámica 1
-- Fuente de normalización: Programa oficial USAC, Escuela de Ingeniería Mecánica, código 390
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Conceptos básicos de la termodinámica',1,'Sistemas cerrados y abiertos; propiedades de un sistema; temperatura y ley cero de la termodinámica.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Conceptos básicos de la termodinámica'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Energía, transferencia de energía y análisis general',2,'Transferencia de energía por calor y trabajo; formas mecánicas de trabajo; primera ley de la termodinámica.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Energía, transferencia de energía y análisis general'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Propiedades de las sustancias puras',3,'Fases; diagramas de propiedades; tablas de propiedades; ecuación de estado de gas ideal.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Propiedades de las sustancias puras'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Análisis de energía de sistemas cerrados',4,'Trabajo de frontera móvil; balance de energía; energía interna, entalpía y calores específicos de gases ideales.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Análisis de energía de sistemas cerrados'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Análisis de masa y energía de volúmenes de control',5,'Conservación de masa; trabajo de flujo; energía de un fluido en movimiento; procesos y dispositivos de flujo estacionario.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=5
      and t.title='Análisis de masa y energía de volúmenes de control'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Segunda ley de la termodinámica',6,'Equilibrio; depósitos de energía térmica; máquinas térmicas; refrigeradores y bombas de calor; ciclo y máquina de Carnot.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=6
      and t.title='Segunda ley de la termodinámica'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Entropía',7,'Entropía; principio de incremento de entropía; cambio de entropía en sustancias puras; procesos isentrópicos.','borrador'
from public.course_programs cp
where cp.course_code='0390'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=7
      and t.title='Entropía'
  );

-- 0524 · Diseño de Máquinas 1
-- Fuente de normalización: Programa oficial USAC, Escuela de Ingeniería Mecánica, código 524
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Principios fundamentales',1,'Equilibrio estático; materiales; tensiones de trabajo; flexión de vigas; momentos de inercia; superposición; deformación y cortadura.','borrador'
from public.course_programs cp
where cp.course_code='0524'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Principios fundamentales'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Tensiones de trabajo',2,'Diagramas tensión-deformación; concentración de tensiones; límite y resistencia a fatiga; tipos de rotura en materiales dúctiles y frágiles.','borrador'
from public.course_programs cp
where cp.course_code='0524'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Tensiones de trabajo'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Ejes',3,'Teorías de falla; cortadura máxima; tensiones normales; teoría de energía de deformación; cargas fijas y alternativas; coeficientes de seguridad.','borrador'
from public.course_programs cp
where cp.course_code='0524'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Ejes'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Resortes',4,'Resortes helicoidales; materiales; diseño óptimo; fatiga; cargas variables; vibración; tolerancias; resortes de compresión y tracción.','borrador'
from public.course_programs cp
where cp.course_code='0524'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Resortes'
  );

-- 0526 · Diseño de Máquinas 2
-- Fuente de normalización: Programa oficial USAC, Escuela de Ingeniería Mecánica, código 526
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Tornillos',1,'Roscas, tolerancias tornillo-tuerca, tornillos de potencia y aplicaciones para transmisión de movimiento y generación de fuerza.','borrador'
from public.course_programs cp
where cp.course_code='0526'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Tornillos'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Fajas, frenos y cadenas',2,'Elementos que utilizan rozamiento o transmisión flexible para transmitir potencia, modificar velocidad y disipar energía.','borrador'
from public.course_programs cp
where cp.course_code='0526'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Fajas, frenos y cadenas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Uniones soldadas y roblonadas',3,'Diseño de juntas y uniones para fabricación de piezas y montaje de estructuras.','borrador'
from public.course_programs cp
where cp.course_code='0526'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Uniones soldadas y roblonadas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Materiales de construcción de elementos de máquinas',4,'Selección y empleo de propiedades de materiales en el diseño de elementos de máquinas.','borrador'
from public.course_programs cp
where cp.course_code='0526'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Materiales de construcción de elementos de máquinas'
  );

-- 0532 · Vibraciones
-- Fuente de normalización: Programa oficial USAC, Escuela de Ingeniería Mecánica, código 532
insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Generalidades del estudio de las vibraciones mecánicas',1,'Definiciones básicas; movimientos periódicos; vibraciones y su origen.','borrador'
from public.course_programs cp
where cp.course_code='0532'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=1
      and t.title='Generalidades del estudio de las vibraciones mecánicas'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Sistemas vibratorios de un grado de libertad',2,'Ecuaciones diferenciales; vibración libre y forzada; sistemas amortiguados y no amortiguados; vibración torsional.','borrador'
from public.course_programs cp
where cp.course_code='0532'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=2
      and t.title='Sistemas vibratorios de un grado de libertad'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Sistemas vibratorios de dos grados de libertad',3,'Ecuaciones diferenciales; formulación matricial; absorbedor dinámico de vibración.','borrador'
from public.course_programs cp
where cp.course_code='0532'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=3
      and t.title='Sistemas vibratorios de dos grados de libertad'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Sistemas vibratorios de varios grados de libertad',4,'Ecuaciones diferenciales; coeficientes de influencia; vibraciones torsionales; desbalance; velocidad crítica; métodos de energía; vibraciones autoexcitadas.','borrador'
from public.course_programs cp
where cp.course_code='0532'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=4
      and t.title='Sistemas vibratorios de varios grados de libertad'
  );

insert into public.topics(course_program_id,parent_id,title,sort_order,body_md,status)
select cp.id,null,'Control de la vibración',5,'Teoría de control; instrumentos de medición de frecuencia, amplitud y aceleración; aisladores; selección y efectividad.','borrador'
from public.course_programs cp
where cp.course_code='0532'
  and cp.version_label='Programa oficial recibido 2026-09-07'
  and not exists (
    select 1 from public.topics t
    where t.course_program_id=cp.id
      and t.sort_order=5
      and t.title='Control de la vibración'
  );

commit;

-- VERIFICACIÓN: los siete cursos deben devolver una cantidad mayor a 0.
select cp.course_code, c.name, count(t.id) as unidades
from public.course_programs cp
join public.courses c on c.code=cp.course_code
left join public.topics t on t.course_program_id=cp.id
where cp.version_label='Programa oficial recibido 2026-09-07'
  and cp.course_code in ('0250','0252','0258','0390','0524','0526','0532')
group by cp.course_code,c.name
order by cp.course_code;