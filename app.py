
import random
import pandas as pd
import streamlit as st

from modules.auth import login, logout
from modules.data import (
    CAREERS, get_areas_for_career, get_courses_for_career,
    get_questions_for_career, COURSES
)
from modules.ui import apply_branding, page_header, metric_card

st.set_page_config(
    page_title="PREP-EIME",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_branding()

def login_view():
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown("## PREP-EIME")
        st.caption("Plataforma de Repaso y Evaluación para el Examen General Privado")
        st.info("Versión inicial institucional · Acceso restringido")
        email = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar", use_container_width=True, type="primary"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciales no válidas o usuario sin acceso.")
        with st.expander("Credenciales de demostración"):
            st.code(
                "estudiante@demo.gt / demo123\n"
                "docente@demo.gt / demo123\n"
                "coordinacion@demo.gt / demo123\n"
                "admin@demo.gt / demo123"
            )

def sidebar(user):
    st.sidebar.markdown("## PREP-EIME")
    st.sidebar.caption("Escuela de Ingeniería Mecánica Eléctrica")
    st.sidebar.markdown("---")
    st.sidebar.write(f"**{user['name']}**")
    st.sidebar.caption(user["role"].capitalize())
    if user.get("career_code"):
        st.sidebar.caption(CAREERS.get(user["career_code"], user["career_code"]))
    if user.get("cohort"):
        st.sidebar.caption(user["cohort"])

    common = ["Inicio", "Preparación académica", "Biblioteca", "Preparación EGP", "Mi progreso"]
    role = user["role"]
    if role == "docente":
        common += ["Gestión académica", "Banco de preguntas"]
    elif role in ("coordinador", "administrador"):
        common += ["Gestión académica", "Usuarios y cohortes", "Analítica"]

    section = st.sidebar.radio("Navegación", common, label_visibility="collapsed")
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar sesión"):
        logout()
    return section

def dashboard_student(user):
    career = user["career_code"]
    courses = get_courses_for_career(career)
    areas = get_areas_for_career(career)
    questions = get_questions_for_career(career)

    page_header(
        f"Bienvenido, {user['name']}",
        f"{CAREERS[career]} · {user.get('cohort','')}"
    )

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Cursos EGP cargados", len(courses), "Estructura inicial")
    with c2: metric_card("Áreas EGP", len(areas), "Según carrera")
    with c3: metric_card("Preguntas disponibles", len(questions), "Banco demo")
    with c4: metric_card("Progreso", "0 %", "Se activará con intentos")

    st.markdown("### Ruta de preparación")
    st.progress(0)
    st.caption("La ruta académica se completará con los programas oficiales de cada curso.")

    st.markdown("### Áreas de preparación")
    cols = st.columns(3)
    for i, area in enumerate(areas):
        with cols[i % 3]:
            st.markdown(
                f'<div class="prep-card"><b>{area}</b><br>'
                f'<span class="prep-muted">Contenido pendiente de validación oficial</span></div>',
                unsafe_allow_html=True
            )

def academic_view(user):
    page_header("Preparación académica", "Navegación por áreas y cursos oficiales")
    if user.get("career_code"):
        career = user["career_code"]
        courses = get_courses_for_career(career)
    else:
        career_name = st.selectbox("Carrera", list(CAREERS.values()))
        career = [k for k,v in CAREERS.items() if v == career_name][0]
        courses = get_courses_for_career(career)

    df = pd.DataFrame(courses)
    if not df.empty:
        df = df[["code","name","semester","area"]].rename(columns={
            "code":"Código","name":"Curso","semester":"Semestre","area":"Área EGP"
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

def library_view(user):
    page_header("Biblioteca académica", "Repositorio institucional del propedéutico")
    st.warning("El repositorio está preparado, pero el contenido académico se incorporará al recibir y validar los programas oficiales.")
    st.markdown("#### Tipos de recurso previstos")
    st.write("PDF, presentaciones, formularios, guías, normas, ejercicios resueltos, enlaces y material docente.")

def egp_view(user):
    page_header("Preparación EGP", "Banco de preguntas y simulador básico")
    if user.get("career_code"):
        qs = get_questions_for_career(user["career_code"])
    else:
        qs = []
        for q in get_questions_for_career("IE") + get_questions_for_career("IEL") + get_questions_for_career("IME"):
            if q not in qs:
                qs.append(q)

    if not qs:
        st.info("Aún no hay preguntas disponibles para este perfil.")
        return

    mode = st.radio("Modo", ["Pregunta aleatoria", "Simulador de 3 preguntas"], horizontal=True)
    if mode == "Pregunta aleatoria":
        q = random.choice(qs)
        st.markdown(f"### {q['question']}")
        st.caption(f"Área: {q['area']} · Dificultad: {q['difficulty']}/5 · Competencia: {q['competency']}")
        st.text_area("Tu respuesta", height=180)
        st.button("Guardar respuesta", type="primary")
    else:
        sample = random.sample(qs, min(3, len(qs)))
        for i,q in enumerate(sample,1):
            st.markdown(f"**{i}. {q['question']}**")
            st.caption(f"{q['area']} · Nivel {q['difficulty']}/5")
            st.text_area(f"Respuesta {i}", key=f"ans_{i}", height=120)
        st.button("Finalizar simulación", type="primary")

def progress_view(user):
    page_header("Mi progreso", "Dominio y actividad")
    st.info("El seguimiento se activará automáticamente cuando se registren intentos, respuestas y evaluaciones.")
    st.progress(0)

def management_view(user):
    page_header("Gestión académica", "Estructura editable de PREP-EIME")
    st.tabs(["Áreas EGP", "Cursos", "Temas", "Recursos"])
    st.dataframe(pd.DataFrame(COURSES), use_container_width=True, hide_index=True)

def users_view(user):
    page_header("Usuarios y cohortes", "Administración de acceso")
    st.info("La versión conectada a Supabase permitirá importar estudiantes desde Excel y activar/desactivar cohortes.")
    sample = pd.DataFrame([
        {"Carné":"202012345","Nombre":"Juan Pérez","Carrera":"Ingeniería Eléctrica","Cohorte":"EGP-2026-II","Estado":"Activo"},
        {"Carné":"202045678","Nombre":"Ana Gómez","Carrera":"Ingeniería Electrónica","Cohorte":"EGP-2026-II","Estado":"Activo"},
    ])
    st.dataframe(sample, use_container_width=True, hide_index=True)

def analytics_view(user):
    page_header("Analítica", "Indicadores de la cohorte")
    c1,c2,c3 = st.columns(3)
    with c1: metric_card("Estudiantes", "0", "Datos reales al conectar Supabase")
    with c2: metric_card("Intentos", "0", "Simulaciones realizadas")
    with c3: metric_card("Dominio promedio", "—", "Sin datos todavía")

if "user" not in st.session_state:
    login_view()
    st.stop()

user = st.session_state.user
section = sidebar(user)

if section == "Inicio":
    if user["role"] == "estudiante":
        dashboard_student(user)
    else:
        page_header(f"Bienvenido, {user['name']}", f"Panel {user['role']}")
        st.success("PREP-EIME v1.0 está operativo en modo demostración.")
        st.write("Utiliza el menú lateral para revisar la estructura académica y administrativa.")
elif section == "Preparación académica":
    academic_view(user)
elif section == "Biblioteca":
    library_view(user)
elif section == "Preparación EGP":
    egp_view(user)
elif section == "Mi progreso":
    progress_view(user)
elif section in ("Gestión académica", "Banco de preguntas"):
    management_view(user)
elif section == "Usuarios y cohortes":
    users_view(user)
elif section == "Analítica":
    analytics_view(user)
