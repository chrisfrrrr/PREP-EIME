import pandas as pd
import streamlit as st

from modules.auth import login, logout
from modules.config import DEMO_MODE
from modules.data import (
    CAREERS, get_careers, get_areas_for_career, get_courses_for_career,
    get_all_courses, get_programs, get_topics_for_program, get_questions_for_career
)
from modules.ui import apply_branding, page_header, metric_card

st.set_page_config(page_title="PREP-EIME", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")
apply_branding()


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
    st.sidebar.caption("PREP-EIME v1.2 · Catálogo académico real")
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
        with c3: metric_card("Estado","Operativo","Base académica conectada")
    st.success("La aplicación ya está leyendo el catálogo académico desde Supabase.")


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

    st.markdown("### Explorar programa y unidades publicadas")
    opts={f"{r['code']} · {r['name']}":r['code'] for r in courses}
    sel=st.selectbox("Curso",list(opts.keys()))
    code=opts[sel]
    programs=[p for p in get_programs(include_drafts=False) if p["course_code"]==code]
    if not programs:
        st.info("El programa está cargado pero todavía no ha sido publicado para estudiantes.")
        return
    p=programs[0]
    st.caption(f"Programa: {p['version_label']} · Estado: {p['status']}")
    topics=get_topics_for_program(p["id"],include_drafts=False)
    for t in topics:
        with st.expander(f"{t['sort_order']}. {t['title']}"):
            st.markdown(t.get("body_md") or "Sin desarrollo adicional.")


def library_view(user):
    page_header("Biblioteca académica","Repositorio institucional")
    st.info("La estructura está lista. Los recursos se incorporarán y publicarán desde Gestión académica en una siguiente versión.")


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


def management_view(user):
    page_header("Gestión académica","Revisión del contenido cargado en Supabase")
    staff=user["role"] in ("docente","coordinador","administrador")
    tabs=st.tabs(["Cursos","Programas","Unidades / temas"])
    with tabs[0]:
        courses=get_all_courses()
        if courses:
            df=pd.DataFrame(courses)[["code","name","semester","area","active"]].rename(columns={"code":"Código","name":"Curso","semester":"Semestre","area":"Área EGP","active":"Activo"})
            st.dataframe(df,use_container_width=True,hide_index=True)
    with tabs[1]:
        programs=get_programs(include_drafts=staff)
        if programs:
            st.dataframe(pd.DataFrame(programs),use_container_width=True,hide_index=True)
        else: st.info("No hay programas visibles con las políticas actuales.")
    with tabs[2]:
        programs=get_programs(include_drafts=staff)
        if not programs: st.info("No hay programas disponibles."); return
        labels={f"{p['course_code']} · {p['version_label']} · {p['status']}":p for p in programs}
        label=st.selectbox("Programa",list(labels.keys()),key="mgmt_program")
        p=labels[label]
        topics=get_topics_for_program(p["id"],include_drafts=staff)
        if topics:
            df=pd.DataFrame(topics)[["sort_order","title","status","body_md"]].rename(columns={"sort_order":"Orden","title":"Unidad / tema","status":"Estado","body_md":"Contenido"})
            st.dataframe(df,use_container_width=True,hide_index=True)
        else: st.info("No hay temas visibles para este programa.")
    st.caption("v1.2 es de revisión/lectura. La edición y publicación desde la interfaz se añadirá tras configurar políticas de escritura por rol.")


def users_view(user):
    page_header("Usuarios y cohortes","Administración de acceso")
    st.info("La administración masiva de estudiantes será el siguiente módulo, con importación desde Excel.")


def analytics_view(user):
    page_header("Analítica","Indicadores iniciales")
    c1,c2=st.columns(2)
    with c1: metric_card("Cursos en catálogo",len(get_all_courses()),"Base real")
    with c2: metric_card("Programas registrados",len(get_programs(include_drafts=True)),"Base real")


if "user" not in st.session_state:
    login_view(); st.stop()
user=st.session_state.user
section=sidebar(user)
if section=="Inicio": home_view(user)
elif section=="Preparación académica": academic_view(user)
elif section=="Biblioteca": library_view(user)
elif section=="Preparación EGP": egp_view(user)
elif section=="Mi progreso": progress_view(user)
elif section in ("Gestión académica","Banco de preguntas"): management_view(user)
elif section=="Usuarios y cohortes": users_view(user)
elif section=="Analítica": analytics_view(user)
