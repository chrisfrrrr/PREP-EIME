import pandas as pd
import streamlit as st

from modules.auth import login, logout
from modules.config import DEMO_MODE
from modules.data import (
    CAREERS, CONTENT_STATUSES, QUESTION_TYPES, COMPETENCIES,
    get_careers, get_areas_for_career, get_courses_for_career,
    get_all_courses, get_all_areas, get_programs, get_topics_for_program,
    get_questions_for_career, get_course_careers, get_topics_for_course,
    get_all_questions, create_question, update_question,
    update_question_status, delete_question,
    update_program_status, update_program_metadata,
    add_topic, update_topic, delete_topic,
)
from modules.ui import apply_branding, page_header, metric_card

st.set_page_config(
    page_title="PREP-EIME",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_branding()

STATUS_LABELS = {
    "borrador": "Borrador",
    "en_revision": "En revisión",
    "aprobado": "Aprobado",
    "publicado": "Publicado",
    "archivado": "Archivado",
}

CAREER_LABELS = {
    "IE": "Ingeniería Eléctrica",
    "IEL": "Ingeniería Electrónica",
    "IME": "Ingeniería Mecánica Eléctrica",
}


def login_view():
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown("## PREP-EIME")
        st.caption("Plataforma de Repaso y Evaluación para el Examen General Privado")
        st.info("Acceso institucional restringido")
        email = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar", use_container_width=True, type="primary"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.rerun()

        if DEMO_MODE:
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

    common = [
        "Inicio",
        "Preparación académica",
        "Biblioteca",
        "Preparación EGP",
        "Mi progreso",
    ]

    if user["role"] == "docente":
        common += ["Gestión académica", "Banco de preguntas"]
    elif user["role"] in ("coordinador", "administrador"):
        common += [
            "Gestión académica",
            "Banco de preguntas",
            "Usuarios y cohortes",
            "Analítica",
        ]

    section = st.sidebar.radio(
        "Navegación", common, label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("PREP-EIME v1.4 · Banco de Preguntas EGP")
    if st.sidebar.button("Cerrar sesión"):
        logout()

    return section


def choose_career(user):
    if user.get("career_code"):
        return user["career_code"]

    careers = get_careers()
    mapping = {x["name"]: x["code"] for x in careers}
    if not mapping:
        return None

    name = st.selectbox("Carrera", list(mapping.keys()))
    return mapping[name]


def _flash(ok, msg):
    if ok:
        st.success(msg)
    else:
        st.error(msg)


def _allowed_transitions(role, status):
    if role == "docente":
        return {
            "borrador": ["en_revision"],
            "en_revision": ["borrador"],
        }.get(status, [])

    if role in ("coordinador", "administrador"):
        return {
            "borrador": ["en_revision"],
            "en_revision": ["borrador", "aprobado"],
            "aprobado": ["en_revision", "publicado"],
            "publicado": ["aprobado", "archivado"],
            "archivado": ["borrador"],
        }.get(status, [])

    return []


def home_view(user):
    page_header(f"Bienvenido, {user['name']}", f"Panel {user['role']}")

    career = choose_career(user) if user["role"] == "estudiante" else None

    if career:
        courses = get_courses_for_career(career)
        areas = get_areas_for_career(career)
        questions = get_questions_for_career(career)

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Cursos EGP", len(courses), "Catálogo institucional")
        with c2:
            metric_card("Áreas EGP", len(areas), "Según carrera")
        with c3:
            metric_card("Preguntas publicadas", len(questions), "Banco EGP")
    else:
        allc = get_all_courses()
        programs = get_programs(include_drafts=True)
        questions = get_all_questions(include_drafts=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Cursos cargados", len(allc), "Supabase")
        with c2:
            metric_card("Programas", len(programs), "Incluye borradores")
        with c3:
            metric_card("Preguntas EGP", len(questions), "Banco institucional")

    st.success("PREP-EIME está conectado al catálogo académico real de Supabase.")


def academic_view(user):
    page_header("Preparación académica", "Ruta por carrera, área y curso")
    career = choose_career(user)

    if not career:
        st.warning("No hay carrera disponible para este perfil.")
        return

    courses = get_courses_for_career(career)
    if not courses:
        st.info("No se encontraron cursos EGP para esta carrera.")
        return

    df = pd.DataFrame(courses)[["code", "name", "semester", "area"]].rename(
        columns={
            "code": "Código",
            "name": "Curso",
            "semester": "Semestre",
            "area": "Área EGP",
        }
    )

    area = st.selectbox(
        "Filtrar por área",
        ["Todas"] + sorted(df["Área EGP"].dropna().unique().tolist()),
    )
    if area != "Todas":
        df = df[df["Área EGP"] == area]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Explorar contenido publicado")
    opts = {f"{r['code']} · {r['name']}": r["code"] for r in courses}
    sel = st.selectbox("Curso", list(opts.keys()))
    code = opts[sel]

    programs = [
        p for p in get_programs(include_drafts=False)
        if p["course_code"] == code
    ]

    if not programs:
        st.info("Este curso todavía no tiene un programa publicado para estudiantes.")
        return

    p = programs[0]
    st.caption(f"Programa: {p['version_label']} · Estado: {p['status']}")

    topics = get_topics_for_program(p["id"], include_drafts=False)
    if not topics:
        st.info("El programa está publicado, pero todavía no contiene unidades publicadas.")

    for t in topics:
        with st.expander(f"{t['sort_order']}. {t['title']}"):
            st.markdown(t.get("body_md") or "Sin desarrollo adicional.")


def library_view(user):
    page_header("Biblioteca académica", "Repositorio institucional")
    st.info(
        "El módulo de recursos se incorporará después de completar "
        "la revisión del banco de preguntas."
    )


def egp_view(user):
    page_header("Preparación EGP", "Preguntas publicadas para práctica")

    career = choose_career(user)
    questions = get_questions_for_career(career) if career else []

    if not questions:
        st.info("Todavía no hay preguntas publicadas para esta carrera.")
        return

    courses = {c["code"]: c for c in get_courses_for_career(career)}

    f1, f2, f3 = st.columns(3)
    with f1:
        area_options = ["Todas"] + sorted({
            courses.get(q.get("course_code"), {}).get("area", "Sin área")
            for q in questions
        })
        area_filter = st.selectbox("Área", area_options)

    with f2:
        course_options = ["Todos"] + sorted({
            q.get("course_code") for q in questions if q.get("course_code")
        })
        course_filter = st.selectbox("Curso", course_options)

    with f3:
        difficulty_filter = st.selectbox("Dificultad", ["Todas", 1, 2, 3, 4, 5])

    filtered = []
    for q in questions:
        c = courses.get(q.get("course_code"), {})
        qarea = c.get("area", "Sin área")
        if area_filter != "Todas" and qarea != area_filter:
            continue
        if course_filter != "Todos" and q.get("course_code") != course_filter:
            continue
        if difficulty_filter != "Todas" and q.get("difficulty") != difficulty_filter:
            continue
        filtered.append(q)

    st.caption(f"{len(filtered)} preguntas disponibles")

    for i, q in enumerate(filtered, 1):
        c = courses.get(q.get("course_code"), {})
        with st.expander(
            f"{i}. {q.get('course_code','')} · "
            f"{c.get('name','')} · Dificultad {q.get('difficulty','—')}/5"
        ):
            st.markdown(f"**Pregunta**")
            st.write(q["question_text"])
            st.caption(
                f"Tipo: {q.get('question_type','—')} · "
                f"Competencia: {q.get('competency','—')}"
            )

            show_key = f"show_answer_{q['id']}"
            if st.button("Mostrar respuesta esperada", key=show_key):
                st.info(q.get("expected_answer") or "No se registró una respuesta esperada.")


def progress_view(user):
    page_header("Mi progreso", "Dominio y actividad")
    st.info(
        "El seguimiento individual se habilitará al activar "
        "simuladores e intentos evaluativos."
    )


def management_view(user):
    page_header("Gestión académica", "Edición, revisión, aprobación y publicación")

    staff = user["role"] in ("docente", "coordinador", "administrador")
    if not staff:
        st.warning("No tienes permisos de gestión académica.")
        return

    courses = get_all_courses()
    programs = get_programs(include_drafts=True)
    course_map = {c["code"]: c for c in courses}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Cursos", len(courses), "Catálogo técnico")
    with c2:
        metric_card("Programas", len(programs), "Versiones registradas")
    with c3:
        metric_card(
            "Publicados",
            sum(1 for p in programs if p["status"] == "publicado"),
            "Visibles a estudiantes",
        )
    with c4:
        metric_card(
            "En revisión",
            sum(1 for p in programs if p["status"] == "en_revision"),
            "Pendientes de decisión",
        )

    tabs = st.tabs(["Mapa académico", "Editor de programa", "Editor de unidades"])

    with tabs[0]:
        if courses:
            rows = []
            p_by_code = {}
            for p in programs:
                p_by_code.setdefault(p["course_code"], []).append(p)

            for c in courses:
                ps = p_by_code.get(c["code"], [])
                rows.append({
                    "Código": c["code"],
                    "Curso": c["name"],
                    "Área EGP": c["area"],
                    "Semestre": c["semester"],
                    "Programas": len(ps),
                    "Estado": ", ".join(sorted({
                        STATUS_LABELS.get(p["status"], p["status"])
                        for p in ps
                    })) if ps else "Sin programa",
                })

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

    with tabs[1]:
        if not programs:
            st.info("No hay programas disponibles.")
        else:
            labels = {}
            for p in programs:
                c = course_map.get(p["course_code"], {})
                labels[
                    f"{p['course_code']} · {c.get('name','')} · "
                    f"{STATUS_LABELS.get(p['status'],p['status'])}"
                ] = p

            label = st.selectbox(
                "Seleccionar programa",
                list(labels.keys()),
                key="editor_program",
            )
            p = labels[label]
            c = course_map.get(p["course_code"], {})

            st.markdown(f"### {p['course_code']} · {c.get('name','Curso')}")
            st.caption(
                f"Área: {c.get('area','Sin área')} · "
                f"Estado actual: {STATUS_LABELS.get(p['status'],p['status'])}"
            )

            with st.form("program_metadata"):
                version = st.text_input(
                    "Versión / identificación",
                    value=p.get("version_label") or "",
                )
                year = st.number_input(
                    "Año de vigencia",
                    min_value=1900,
                    max_value=2100,
                    value=int(p.get("effective_year") or 2026),
                    step=1,
                )
                source = st.text_area(
                    "Fuente / observación",
                    value=p.get("source_note") or "",
                    height=90,
                )
                save = st.form_submit_button(
                    "Guardar metadatos",
                    type="primary",
                )
                if save:
                    ok, msg = update_program_metadata(
                        p["id"], version, year, source
                    )
                    _flash(ok, msg)
                    if ok:
                        st.rerun()

            st.markdown("#### Flujo editorial")
            transitions = _allowed_transitions(user["role"], p["status"])

            if not transitions:
                st.caption(
                    "No hay transiciones disponibles para tu rol "
                    "desde el estado actual."
                )
            else:
                cols = st.columns(len(transitions))
                for col, target in zip(cols, transitions):
                    with col:
                        if st.button(
                            f"→ {STATUS_LABELS[target]}",
                            use_container_width=True,
                            key=f"pstatus_{p['id']}_{target}",
                        ):
                            ok, msg = update_program_status(p["id"], target)
                            _flash(ok, msg)
                            if ok:
                                st.rerun()

    with tabs[2]:
        if not programs:
            st.info("No hay programas disponibles.")
        else:
            labels = {}
            for p in programs:
                c = course_map.get(p["course_code"], {})
                labels[
                    f"{p['course_code']} · {c.get('name','')} · "
                    f"{STATUS_LABELS.get(p['status'],p['status'])}"
                ] = p

            label = st.selectbox(
                "Programa",
                list(labels.keys()),
                key="topic_program",
            )
            p = labels[label]
            topics = get_topics_for_program(p["id"], include_drafts=True)

            st.markdown("#### Unidades / temas existentes")
            if not topics:
                st.info("Este programa no tiene unidades registradas.")

            for t in topics:
                with st.expander(
                    f"{t['sort_order']}. {t['title']} · "
                    f"{STATUS_LABELS.get(t['status'],t['status'])}"
                ):
                    with st.form(f"topic_{t['id']}"):
                        title = st.text_input(
                            "Título",
                            value=t.get("title") or "",
                            key=f"title_{t['id']}",
                        )
                        order = st.number_input(
                            "Orden",
                            min_value=0,
                            max_value=999,
                            value=int(t.get("sort_order") or 0),
                            step=1,
                            key=f"order_{t['id']}",
                        )
                        body = st.text_area(
                            "Contenido",
                            value=t.get("body_md") or "",
                            height=260,
                            key=f"body_{t['id']}",
                        )

                        allowed_status = (
                            ["borrador", "en_revision"]
                            if user["role"] == "docente"
                            else list(STATUS_LABELS.keys())
                        )
                        current = t.get("status") or "borrador"
                        if current not in allowed_status:
                            allowed_status = [current] + [
                                x for x in allowed_status if x != current
                            ]

                        status = st.selectbox(
                            "Estado",
                            allowed_status,
                            index=allowed_status.index(current),
                            format_func=lambda x: STATUS_LABELS[x],
                            key=f"status_{t['id']}",
                        )

                        save_topic = st.form_submit_button(
                            "Guardar unidad / tema",
                            type="primary",
                        )

                        if save_topic:
                            ok, msg = update_topic(
                                t["id"], title, order, body, status
                            )
                            _flash(ok, msg)
                            if ok:
                                st.rerun()

                    if user["role"] == "administrador":
                        if st.button(
                            "Eliminar unidad / tema",
                            key=f"del_{t['id']}",
                        ):
                            ok, msg = delete_topic(t["id"])
                            _flash(ok, msg)
                            if ok:
                                st.rerun()

            st.markdown("#### Agregar nueva unidad / tema")
            with st.form("new_topic_form"):
                nt = st.text_input("Título de la nueva unidad")
                no = st.number_input(
                    "Orden",
                    min_value=0,
                    max_value=999,
                    value=(
                        max([
                            int(x.get("sort_order") or 0)
                            for x in topics
                        ], default=0) + 1
                    ),
                    step=1,
                )
                nb = st.text_area("Contenido inicial", height=180)
                submitted = st.form_submit_button(
                    "Crear unidad / tema",
                    type="primary",
                )

                if submitted:
                    ok, msg = add_topic(
                        p["id"], nt, no, nb, "borrador"
                    )
                    _flash(ok, msg)
                    if ok:
                        st.rerun()

    st.caption(
        "Regla editorial: docente prepara y envía a revisión; "
        "coordinación/administración aprueba y publica."
    )


def question_bank_view(user):
    page_header(
        "Banco de preguntas EGP",
        "Creación, clasificación, revisión y publicación de preguntas",
    )

    if user["role"] not in ("docente", "coordinador", "administrador"):
        st.warning("No tienes permisos para administrar el banco.")
        return

    courses = get_all_courses()
    areas = get_all_areas()
    questions = get_all_questions(include_drafts=True)

    course_map = {c["code"]: c for c in courses}
    area_map = {a["id"]: a["name"] for a in areas}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total", len(questions), "Preguntas registradas")
    with c2:
        metric_card(
            "Borradores",
            sum(1 for q in questions if q["status"] == "borrador"),
            "En elaboración",
        )
    with c3:
        metric_card(
            "En revisión",
            sum(1 for q in questions if q["status"] == "en_revision"),
            "Pendientes",
        )
    with c4:
        metric_card(
            "Publicadas",
            sum(1 for q in questions if q["status"] == "publicado"),
            "Disponibles al estudiante",
        )

    tabs = st.tabs([
        "Explorar banco",
        "Crear pregunta",
        "Editar / flujo editorial",
    ])

    with tabs[0]:
        if not questions:
            st.info("El banco todavía está vacío.")
        else:
            f1, f2, f3, f4 = st.columns(4)

            with f1:
                career_filter = st.selectbox(
                    "Carrera",
                    ["Todas", "IE", "IEL", "IME"],
                    format_func=lambda x: (
                        "Todas" if x == "Todas"
                        else f"{x} · {CAREER_LABELS[x]}"
                    ),
                    key="qb_filter_career",
                )

            with f2:
                area_names = ["Todas"] + sorted(set(area_map.values()))
                area_filter = st.selectbox(
                    "Área EGP",
                    area_names,
                    key="qb_filter_area",
                )

            with f3:
                status_filter = st.selectbox(
                    "Estado",
                    ["Todos"] + list(STATUS_LABELS.keys()),
                    format_func=lambda x: (
                        "Todos" if x == "Todos"
                        else STATUS_LABELS[x]
                    ),
                    key="qb_filter_status",
                )

            with f4:
                difficulty_filter = st.selectbox(
                    "Dificultad",
                    ["Todas", 1, 2, 3, 4, 5],
                    key="qb_filter_diff",
                )

            rows = []
            filtered = []

            for q in questions:
                c = course_map.get(q.get("course_code"), {})
                qarea = area_map.get(q.get("area_id"), c.get("area", "Sin área"))
                careers = q.get("careers", [])

                if career_filter != "Todas" and career_filter not in careers:
                    continue
                if area_filter != "Todas" and qarea != area_filter:
                    continue
                if status_filter != "Todos" and q["status"] != status_filter:
                    continue
                if difficulty_filter != "Todas" and q.get("difficulty") != difficulty_filter:
                    continue

                filtered.append(q)
                rows.append({
                    "Curso": q.get("course_code"),
                    "Área EGP": qarea,
                    "Carreras": ", ".join(careers),
                    "Tipo": q.get("question_type"),
                    "Competencia": q.get("competency"),
                    "Dificultad": q.get("difficulty"),
                    "Estado": STATUS_LABELS.get(q["status"], q["status"]),
                    "Pregunta": q["question_text"][:140],
                })

            st.caption(f"{len(filtered)} preguntas encontradas")

            if rows:
                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                )

            for q in filtered[:30]:
                c = course_map.get(q.get("course_code"), {})
                with st.expander(
                    f"{q.get('course_code','')} · {c.get('name','')} · "
                    f"{STATUS_LABELS.get(q['status'],q['status'])}"
                ):
                    st.markdown("**Pregunta**")
                    st.write(q["question_text"])
                    st.markdown("**Respuesta esperada / criterio**")
                    st.write(
                        q.get("expected_answer")
                        or "Sin respuesta esperada registrada."
                    )
                    st.caption(
                        f"Carreras: {', '.join(q.get('careers', []))} · "
                        f"Dificultad: {q.get('difficulty','—')}/5 · "
                        f"Competencia: {q.get('competency','—')} · "
                        f"Tipo: {q.get('question_type','—')}"
                    )

    with tabs[1]:
        st.markdown("### Nueva pregunta")

        course_labels = {
            f"{c['code']} · {c['name']}": c
            for c in courses
        }

        if not course_labels:
            st.warning("No hay cursos disponibles.")
        else:
            course_label = st.selectbox(
                "Curso",
                list(course_labels.keys()),
                key="newq_course",
            )
            course = course_labels[course_label]

            course_area = next(
                (a for a in areas if a["id"] == course.get("area_id")),
                None,
            )
            default_area_id = course_area["id"] if course_area else None

            linked_careers = get_course_careers(course["code"])
            topics = get_topics_for_course(
                course["code"],
                include_drafts=True,
            )

            topic_labels = {"Sin tema específico": None}
            for t in topics:
                topic_labels[
                    f"{t.get('sort_order',0)} · {t['title']} "
                    f"[{STATUS_LABELS.get(t['status'],t['status'])}]"
                ] = t["id"]

            with st.form("create_question_form"):
                st.caption(
                    f"Área EGP: {course.get('area','Sin área')} · "
                    f"Carreras vinculadas al curso: "
                    f"{', '.join(linked_careers) or 'Ninguna'}"
                )

                topic_label = st.selectbox(
                    "Unidad / tema",
                    list(topic_labels.keys()),
                )
                question_text = st.text_area(
                    "Enunciado de la pregunta",
                    height=180,
                    placeholder=(
                        "Formule una pregunta que evalúe comprensión, "
                        "cálculo, análisis o defensa técnica."
                    ),
                )
                expected_answer = st.text_area(
                    "Respuesta esperada / criterio de evaluación",
                    height=180,
                    placeholder=(
                        "Incluya los elementos mínimos que debería "
                        "contener una respuesta técnicamente correcta."
                    ),
                )

                q1, q2, q3 = st.columns(3)
                with q1:
                    difficulty = st.select_slider(
                        "Dificultad",
                        options=[1, 2, 3, 4, 5],
                        value=3,
                    )
                with q2:
                    competency = st.selectbox(
                        "Competencia",
                        COMPETENCIES,
                    )
                with q3:
                    question_type = st.selectbox(
                        "Tipo",
                        QUESTION_TYPES,
                    )

                careers = st.multiselect(
                    "Carreras donde aplica",
                    options=["IE", "IEL", "IME"],
                    default=linked_careers,
                    format_func=lambda x: f"{x} · {CAREER_LABELS[x]}",
                )

                create = st.form_submit_button(
                    "Crear como borrador",
                    type="primary",
                    use_container_width=True,
                )

                if create:
                    ok, msg, qid = create_question(
                        area_id=default_area_id,
                        course_code=course["code"],
                        topic_id=topic_labels[topic_label],
                        question_text=question_text,
                        expected_answer=expected_answer,
                        difficulty=difficulty,
                        competency=competency,
                        question_type=question_type,
                        career_codes=careers,
                        created_by=user["id"],
                    )
                    _flash(ok, msg)
                    if ok:
                        st.rerun()

    with tabs[2]:
        if not questions:
            st.info("No hay preguntas para editar.")
        else:
            labels = {}
            for q in questions:
                c = course_map.get(q.get("course_code"), {})
                preview = q["question_text"].replace("\n", " ")[:85]
                labels[
                    f"{q.get('course_code','')} · "
                    f"{STATUS_LABELS.get(q['status'],q['status'])} · "
                    f"{preview}"
                ] = q

            label = st.selectbox(
                "Seleccionar pregunta",
                list(labels.keys()),
                key="edit_question_selector",
            )
            q = labels[label]
            course = course_map.get(q.get("course_code"), {})

            st.markdown(
                f"### {q.get('course_code','')} · "
                f"{course.get('name','Pregunta EGP')}"
            )

            course_labels = {
                f"{c['code']} · {c['name']}": c
                for c in courses
            }
            current_course_label = next(
                (
                    lbl for lbl, c in course_labels.items()
                    if c["code"] == q.get("course_code")
                ),
                list(course_labels.keys())[0],
            )

            selected_course_label = st.selectbox(
                "Curso",
                list(course_labels.keys()),
                index=list(course_labels.keys()).index(current_course_label),
                key=f"edit_course_{q['id']}",
            )
            selected_course = course_labels[selected_course_label]

            topics = get_topics_for_course(
                selected_course["code"],
                include_drafts=True,
            )
            topic_labels = {"Sin tema específico": None}
            for t in topics:
                topic_labels[
                    f"{t.get('sort_order',0)} · {t['title']}"
                ] = t["id"]

            current_topic_label = next(
                (
                    lbl for lbl, tid in topic_labels.items()
                    if tid == q.get("topic_id")
                ),
                "Sin tema específico",
            )

            area_id = selected_course.get("area_id")
            recommended_careers = get_course_careers(
                selected_course["code"]
            )

            with st.form(f"edit_question_form_{q['id']}"):
                topic_label = st.selectbox(
                    "Unidad / tema",
                    list(topic_labels.keys()),
                    index=list(topic_labels.keys()).index(current_topic_label),
                )

                question_text = st.text_area(
                    "Enunciado",
                    value=q.get("question_text") or "",
                    height=180,
                )
                expected_answer = st.text_area(
                    "Respuesta esperada / criterio",
                    value=q.get("expected_answer") or "",
                    height=180,
                )

                e1, e2, e3 = st.columns(3)
                with e1:
                    difficulty = st.select_slider(
                        "Dificultad",
                        options=[1, 2, 3, 4, 5],
                        value=int(q.get("difficulty") or 3),
                    )
                with e2:
                    current_comp = (
                        q.get("competency")
                        if q.get("competency") in COMPETENCIES
                        else COMPETENCIES[0]
                    )
                    competency = st.selectbox(
                        "Competencia",
                        COMPETENCIES,
                        index=COMPETENCIES.index(current_comp),
                    )
                with e3:
                    current_type = (
                        q.get("question_type")
                        if q.get("question_type") in QUESTION_TYPES
                        else QUESTION_TYPES[0]
                    )
                    question_type = st.selectbox(
                        "Tipo",
                        QUESTION_TYPES,
                        index=QUESTION_TYPES.index(current_type),
                    )

                careers = st.multiselect(
                    "Carreras donde aplica",
                    options=["IE", "IEL", "IME"],
                    default=q.get("careers") or recommended_careers,
                    format_func=lambda x: f"{x} · {CAREER_LABELS[x]}",
                )

                allowed_status = (
                    ["borrador", "en_revision"]
                    if user["role"] == "docente"
                    else list(STATUS_LABELS.keys())
                )
                current_status = q["status"]
                if current_status not in allowed_status:
                    allowed_status = [current_status] + [
                        x for x in allowed_status
                        if x != current_status
                    ]

                status = st.selectbox(
                    "Estado",
                    allowed_status,
                    index=allowed_status.index(current_status),
                    format_func=lambda x: STATUS_LABELS[x],
                )

                save = st.form_submit_button(
                    "Guardar cambios",
                    type="primary",
                )

                if save:
                    ok, msg = update_question(
                        question_id=q["id"],
                        area_id=area_id,
                        course_code=selected_course["code"],
                        topic_id=topic_labels[topic_label],
                        question_text=question_text,
                        expected_answer=expected_answer,
                        difficulty=difficulty,
                        competency=competency,
                        question_type=question_type,
                        status=status,
                        career_codes=careers,
                    )
                    _flash(ok, msg)
                    if ok:
                        st.rerun()

            st.markdown("#### Flujo editorial")
            transitions = _allowed_transitions(
                user["role"],
                q["status"],
            )

            if transitions:
                cols = st.columns(len(transitions))
                for col, target in zip(cols, transitions):
                    with col:
                        if st.button(
                            f"→ {STATUS_LABELS[target]}",
                            use_container_width=True,
                            key=f"qstatus_{q['id']}_{target}",
                        ):
                            ok, msg = update_question_status(
                                q["id"],
                                target,
                            )
                            _flash(ok, msg)
                            if ok:
                                st.rerun()
            else:
                st.caption(
                    "No hay transiciones editoriales disponibles "
                    "desde el estado actual para tu rol."
                )

            if user["role"] == "administrador":
                st.markdown("---")
                confirm = st.checkbox(
                    "Confirmo que deseo habilitar la eliminación",
                    key=f"confirm_delete_q_{q['id']}",
                )
                if st.button(
                    "Eliminar pregunta",
                    disabled=not confirm,
                    key=f"delete_q_{q['id']}",
                ):
                    ok, msg = delete_question(q["id"])
                    _flash(ok, msg)
                    if ok:
                        st.rerun()

    st.caption(
        "Modelo recomendado: cada pregunta debe estar vinculada a curso, "
        "tema cuando corresponda, carrera(s), dificultad, competencia y "
        "respuesta esperada."
    )


def users_view(user):
    page_header("Usuarios y cohortes", "Administración de acceso")
    st.info(
        "La administración masiva de estudiantes será una etapa posterior, "
        "con importación desde Excel."
    )


def analytics_view(user):
    page_header("Analítica", "Indicadores iniciales")

    programs = get_programs(include_drafts=True)
    questions = get_all_questions(include_drafts=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(
            "Cursos en catálogo",
            len(get_all_courses()),
            "Base real",
        )
    with c2:
        metric_card(
            "Programas registrados",
            len(programs),
            "Base real",
        )
    with c3:
        metric_card(
            "Preguntas EGP",
            len(questions),
            "Banco real",
        )
    with c4:
        metric_card(
            "Preguntas publicadas",
            sum(1 for q in questions if q["status"] == "publicado"),
            "Disponibles al estudiante",
        )


if "user" not in st.session_state:
    login_view()
    st.stop()

user = st.session_state.user
section = sidebar(user)

if section == "Inicio":
    home_view(user)
elif section == "Preparación académica":
    academic_view(user)
elif section == "Biblioteca":
    library_view(user)
elif section == "Preparación EGP":
    egp_view(user)
elif section == "Mi progreso":
    progress_view(user)
elif section == "Gestión académica":
    management_view(user)
elif section == "Banco de preguntas":
    question_bank_view(user)
elif section == "Usuarios y cohortes":
    users_view(user)
elif section == "Analítica":
    analytics_view(user)
