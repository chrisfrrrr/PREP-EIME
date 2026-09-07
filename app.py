import pandas as pd
import streamlit as st

from modules.auth import login, logout
from modules.config import DEMO_MODE
from modules.data import (
    CAREERS, get_careers, get_areas_for_career, get_courses_for_career,
    get_all_courses, get_programs, get_topics_for_program, get_questions_for_career,
    update_program_status, update_program_metadata, add_topic, update_topic, delete_topic
)
from modules.ui import apply_branding, page_header, metric_card

st.set_page_config(page_title="PREP-EIME", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")
apply_branding()

STATUS_LABELS={
    "borrador":"Borrador",
    "en_revision":"En revisión",
    "aprobado":"Aprobado",
    "publicado":"Publicado",
    "archivado":"Archivado",
}


def login_view():
    c1,c2,c3=st.columns([1,1.3,1])
    with c2:
        st.markdown("## PREP-EIME")
        st.caption("Plataforma de Repaso y Evaluación para el Examen General Privado")
        st.info("Acceso institucional restringido")
        email=st.text_input("Correo")
        password=st.text_input("Contraseña",type="password")
        if st.button("Ingresar",use_container_width=True,type="primary"):
            user=login(email,password)
            if user:
                st.session_state.user=user
                st.rerun()
        if DEMO_MODE:
            with st.expander("Credenciales de demostración"):
                st.code("estudiante@demo.gt / demo123\ndocente@demo.gt / demo123\ncoordinacion@demo.gt / demo123\nadmin@demo.gt / demo123")


def sidebar(user):
    st.sidebar.markdown("## PREP-EIME")
    st.sidebar.caption("Escuela de Ingeniería Mecánica Eléctrica")
    st.sidebar.markdown("---")
    st.sidebar.write(f"**{user['name']}**")
    st.sidebar.caption(user["role"].capitalize())
    if user.get("career_code"): st.sidebar.caption(CAREERS.get(user["career_code"],user["career_code"]))
    if user.get("cohort"): st.sidebar.caption(user["cohort"])
    common=["Inicio","Preparación académica","Biblioteca","Preparación EGP","Mi progreso"]
    if user["role"]=="docente": common += ["Gestión académica","Banco de preguntas"]
    elif user["role"] in ("coordinador","administrador"): common += ["Gestión académica","Usuarios y cohortes","Analítica"]
    section=st.sidebar.radio("Navegación",common,label_visibility="collapsed")
    st.sidebar.markdown("---")
    st.sidebar.caption("PREP-EIME v1.3 · Gestor académico")
    if st.sidebar.button("Cerrar sesión"): logout()
    return section


def choose_career(user):
    if user.get("career_code"):
        return user["career_code"]
    careers=get_careers()
    mapping={x["name"]:x["code"] for x in careers}
    if not mapping: return None
    name=st.selectbox("Carrera",list(mapping.keys()))
    return mapping[name]


def home_view(user):
    page_header(f"Bienvenido, {user['name']}", f"Panel {user['role']}")
    career=choose_career(user) if user["role"]=="estudiante" else None
    if career:
        courses=get_courses_for_career(career); areas=get_areas_for_career(career)
        c1,c2,c3=st.columns(3)
        with c1: metric_card("Cursos EGP",len(courses),"Catálogo institucional")
        with c2: metric_card("Áreas EGP",len(areas),"Según carrera")
        with c3: metric_card("Preguntas publicadas",len(get_questions_for_career(career)),"Banco EGP")
    else:
        allc=get_all_courses(); programs=get_programs(include_drafts=True)
        c1,c2,c3=st.columns(3)
        with c1: metric_card("Cursos cargados",len(allc),"Supabase")
        with c2: metric_card("Programas",len(programs),"Incluye borradores")
        with c3: metric_card("Estado","Operativo","Gestor académico conectado")
    st.success("PREP-EIME está operando sobre el catálogo académico real de Supabase.")


def academic_view(user):
    page_header("Preparación académica","Ruta por carrera, área y curso")
    career=choose_career(user)
    if not career:
        st.warning("No hay carrera disponible para este perfil."); return
    courses=get_courses_for_career(career)
    if not courses:
        st.info("No se encontraron cursos EGP para esta carrera."); return
    df=pd.DataFrame(courses)[["code","name","semester","area"]].rename(columns={"code":"Código","name":"Curso","semester":"Semestre","area":"Área EGP"})
    area=st.selectbox("Filtrar por área",["Todas"]+sorted(df["Área EGP"].dropna().unique().tolist()))
    if area!="Todas": df=df[df["Área EGP"]==area]
    st.dataframe(df,use_container_width=True,hide_index=True)

    st.markdown("### Explorar contenido publicado")
    opts={f"{r['code']} · {r['name']}":r['code'] for r in courses}
    sel=st.selectbox("Curso",list(opts.keys()))
    code=opts[sel]
    programs=[p for p in get_programs(include_drafts=False) if p["course_code"]==code]
    if not programs:
        st.info("Este curso todavía no tiene un programa publicado para estudiantes.")
        return
    p=programs[0]
    st.caption(f"Programa: {p['version_label']} · Estado: {p['status']}")
    topics=get_topics_for_program(p["id"],include_drafts=False)
    if not topics:
        st.info("El programa está publicado, pero todavía no contiene unidades publicadas.")
    for t in topics:
        with st.expander(f"{t['sort_order']}. {t['title']}"):
            st.markdown(t.get("body_md") or "Sin desarrollo adicional.")


def library_view(user):
    page_header("Biblioteca académica","Repositorio institucional")
    st.info("El módulo de recursos se incorporará después de completar la revisión/publicación del contenido académico.")


def egp_view(user):
    page_header("Preparación EGP","Banco de preguntas")
    career=choose_career(user)
    qs=get_questions_for_career(career) if career else []
    if not qs:
        st.info("Todavía no hay preguntas publicadas para esta carrera.")
        return
    for i,q in enumerate(qs[:20],1):
        with st.expander(f"Pregunta {i} · {q.get('course_code','')}"):
            st.write(q["question_text"])
            st.caption(f"Dificultad: {q.get('difficulty','—')}/5 · Competencia: {q.get('competency','—')}")


def progress_view(user):
    page_header("Mi progreso","Dominio y actividad")
    st.info("El seguimiento individual se habilitará al activar intentos y evaluaciones.")


def _allowed_transitions(role,status):
    if role=="docente":
        return {
            "borrador":["en_revision"],
            "en_revision":["borrador"],
        }.get(status,[])
    if role in ("coordinador","administrador"):
        return {
            "borrador":["en_revision"],
            "en_revision":["borrador","aprobado"],
            "aprobado":["en_revision","publicado"],
            "publicado":["aprobado","archivado"],
            "archivado":["borrador"],
        }.get(status,[])
    return []


def _flash(ok,msg):
    if ok: st.success(msg)
    else: st.error(msg)


def management_view(user):
    page_header("Gestión académica","Edición, revisión, aprobación y publicación")
    staff=user["role"] in ("docente","coordinador","administrador")
    if not staff:
        st.warning("No tienes permisos de gestión académica.")
        return

    courses=get_all_courses()
    programs=get_programs(include_drafts=True)
    course_map={c["code"]:c for c in courses}

    c1,c2,c3,c4=st.columns(4)
    with c1: metric_card("Cursos",len(courses),"Catálogo técnico")
    with c2: metric_card("Programas",len(programs),"Versiones registradas")
    with c3: metric_card("Publicados",sum(1 for p in programs if p["status"]=="publicado"),"Visibles a estudiantes")
    with c4: metric_card("En revisión",sum(1 for p in programs if p["status"]=="en_revision"),"Pendientes de decisión")

    tabs=st.tabs(["Mapa académico","Editor de programa","Editor de unidades"])
    with tabs[0]:
        if courses:
            rows=[]
            p_by_code={}
            for p in programs:
                p_by_code.setdefault(p["course_code"],[]).append(p)
            for c in courses:
                ps=p_by_code.get(c["code"],[])
                rows.append({
                    "Código":c["code"],"Curso":c["name"],"Área EGP":c["area"],
                    "Semestre":c["semester"],
                    "Programas":len(ps),
                    "Estado":", ".join(sorted({STATUS_LABELS.get(p["status"],p["status"]) for p in ps})) if ps else "Sin programa"
                })
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    with tabs[1]:
        if not programs:
            st.info("No hay programas disponibles."); 
        else:
            labels={}
            for p in programs:
                c=course_map.get(p["course_code"],{})
                labels[f"{p['course_code']} · {c.get('name','')} · {STATUS_LABELS.get(p['status'],p['status'])}"]=p
            label=st.selectbox("Seleccionar programa",list(labels.keys()),key="editor_program")
            p=labels[label]
            c=course_map.get(p["course_code"],{})
            st.markdown(f"### {p['course_code']} · {c.get('name','Curso')}")
            st.caption(f"Área: {c.get('area','Sin área')} · Estado actual: {STATUS_LABELS.get(p['status'],p['status'])}")

            with st.form("program_metadata"):
                version=st.text_input("Versión / identificación",value=p.get("version_label") or "")
                year=st.number_input("Año de vigencia",min_value=1900,max_value=2100,value=int(p.get("effective_year") or 2026),step=1)
                source=st.text_area("Fuente / observación",value=p.get("source_note") or "",height=90)
                save=st.form_submit_button("Guardar metadatos",type="primary")
                if save:
                    ok,msg=update_program_metadata(p["id"],version,year,source)
                    _flash(ok,msg)
                    if ok: st.rerun()

            st.markdown("#### Flujo editorial")
            transitions=_allowed_transitions(user["role"],p["status"])
            if not transitions:
                st.caption("No hay transiciones disponibles para tu rol desde el estado actual.")
            else:
                cols=st.columns(len(transitions))
                for col,target in zip(cols,transitions):
                    with col:
                        if st.button(f"→ {STATUS_LABELS[target]}",use_container_width=True,key=f"pstatus_{p['id']}_{target}"):
                            ok,msg=update_program_status(p["id"],target)
                            _flash(ok,msg)
                            if ok: st.rerun()

            if p["status"]=="publicado":
                st.success("Este programa ya puede ser consultado por estudiantes.")
            elif p["status"]=="aprobado":
                st.info("Programa aprobado. Coordinación/administración puede publicarlo.")
            elif p["status"]=="en_revision":
                st.warning("Programa en revisión académica.")
            else:
                st.info("Programa en borrador. Puede editarse antes de enviarlo a revisión.")

    with tabs[2]:
        if not programs:
            st.info("No hay programas disponibles.")
        else:
            labels={}
            for p in programs:
                c=course_map.get(p["course_code"],{})
                labels[f"{p['course_code']} · {c.get('name','')} · {STATUS_LABELS.get(p['status'],p['status'])}"]=p
            label=st.selectbox("Programa",list(labels.keys()),key="topic_program")
            p=labels[label]
            topics=get_topics_for_program(p["id"],include_drafts=True)

            st.markdown("#### Unidades / temas existentes")
            if not topics:
                st.info("Este programa no tiene unidades registradas.")
            for t in topics:
                with st.expander(f"{t['sort_order']}. {t['title']} · {STATUS_LABELS.get(t['status'],t['status'])}"):
                    with st.form(f"topic_{t['id']}"):
                        title=st.text_input("Título",value=t.get("title") or "",key=f"title_{t['id']}")
                        order=st.number_input("Orden",min_value=0,max_value=999,value=int(t.get("sort_order") or 0),step=1,key=f"order_{t['id']}")
                        body=st.text_area("Contenido",value=t.get("body_md") or "",height=260,key=f"body_{t['id']}")
                        allowed_status=["borrador","en_revision"] if user["role"]=="docente" else list(STATUS_LABELS.keys())
                        current=t.get("status") or "borrador"
                        if current not in allowed_status:
                            allowed_status=[current]+[x for x in allowed_status if x!=current]
                        status=st.selectbox("Estado",allowed_status,index=allowed_status.index(current),format_func=lambda x:STATUS_LABELS[x],key=f"status_{t['id']}")
                        save_topic=st.form_submit_button("Guardar unidad / tema",type="primary")
                        if save_topic:
                            ok,msg=update_topic(t["id"],title,order,body,status)
                            _flash(ok,msg)
                            if ok: st.rerun()
                    if user["role"]=="administrador":
                        if st.button("Eliminar unidad / tema",key=f"del_{t['id']}"):
                            ok,msg=delete_topic(t["id"])
                            _flash(ok,msg)
                            if ok: st.rerun()

            st.markdown("#### Agregar nueva unidad / tema")
            with st.form("new_topic_form"):
                nt=st.text_input("Título de la nueva unidad")
                no=st.number_input("Orden",min_value=0,max_value=999,value=(max([int(x.get("sort_order") or 0) for x in topics],default=0)+1),step=1)
                nb=st.text_area("Contenido inicial",height=180)
                submitted=st.form_submit_button("Crear unidad / tema",type="primary")
                if submitted:
                    ok,msg=add_topic(p["id"],nt,no,nb,"borrador")
                    _flash(ok,msg)
                    if ok: st.rerun()

    st.caption("Regla editorial: docente prepara y envía a revisión; coordinación/administración aprueba y publica; administrador puede eliminar.")


def users_view(user):
    page_header("Usuarios y cohortes","Administración de acceso")
    st.info("La administración masiva de estudiantes será el siguiente módulo, con importación desde Excel.")


def analytics_view(user):
    page_header("Analítica","Indicadores iniciales")
    programs=get_programs(include_drafts=True)
    c1,c2,c3=st.columns(3)
    with c1: metric_card("Cursos en catálogo",len(get_all_courses()),"Base real")
    with c2: metric_card("Programas registrados",len(programs),"Base real")
    with c3: metric_card("Programas publicados",sum(1 for p in programs if p["status"]=="publicado"),"Visibles a estudiantes")


if "user" not in st.session_state:
    login_view(); st.stop()
user=st.session_state.user
section=sidebar(user)
if section=="Inicio": home_view(user)
elif section=="Preparación académica": academic_view(user)
elif section=="Biblioteca": library_view(user)
elif section=="Preparación EGP": egp_view(user)
elif section=="Mi progreso": progress_view(user)
elif section=="Gestión académica": management_view(user)
elif section=="Banco de preguntas": 
    page_header("Banco de preguntas","Módulo siguiente")
    st.info("La estructura de preguntas ya existe. El editor de preguntas será la siguiente etapa después de validar el flujo editorial académico.")
elif section=="Usuarios y cohortes": users_view(user)
elif section=="Analítica": analytics_view(user)
