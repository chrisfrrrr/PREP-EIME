import streamlit as st
from .config import DEMO_MODE
from .supabase_client import get_supabase_client

CAREERS = {
    "IME": "Ingeniería Mecánica Eléctrica",
    "IE": "Ingeniería Eléctrica",
    "IEL": "Ingeniería Electrónica",
}

DEMO_USERS = {
    "estudiante@demo.gt": {"password":"demo123","name":"Juan Pérez","role":"estudiante","career_code":"IE","cohort":"EGP-2026-II","student_id":"202012345"},
    "docente@demo.gt": {"password":"demo123","name":"Ing. María López","role":"docente","career_code":"IE","cohort":"EGP-2026-II"},
    "coordinacion@demo.gt": {"password":"demo123","name":"Coordinación EIME","role":"coordinador","career_code":None,"cohort":"EGP-2026-II"},
    "admin@demo.gt": {"password":"demo123","name":"Administrador PREP-EIME","role":"administrador","career_code":None,"cohort":"EGP-2026-II"},
}

DEMO_QUESTIONS = []


def _client():
    return get_supabase_client(require_auth=True)


def _fetch_all_pages(query_factory, *, order_column="id", desc=False, page_size=500):
    """Retrieve all PostgREST rows in bounded pages, avoiding the default 1,000-row cap.

    query_factory must create a fresh query each time; ordering must be stable.
    Exceptions propagate so a failed page cannot silently appear as complete data.
    """
    rows = []
    offset = 0
    while True:
        query = query_factory().order(order_column, desc=desc)
        batch = query.range(offset, offset + page_size - 1).execute().data or []
        rows.extend(batch)
        if len(batch) < page_size:
            return rows
        offset += page_size


def _fetch_questions_by_ids(client, ids, columns, *, published_only=False):
    """Bound IN filters and paginate each result set for large career question banks."""
    result = []
    unique_ids = list(dict.fromkeys(ids))
    for start in range(0, len(unique_ids), 200):
        chunk = unique_ids[start:start + 200]
        def query():
            q = client.table("questions").select(columns).in_("id", chunk)
            return q.eq("status", "publicado") if published_only else q
        result.extend(_fetch_all_pages(query))
    return result


def get_careers():
    if DEMO_MODE:
        return [{"code": k, "name": v} for k,v in CAREERS.items()]
    c=_client()
    if not c: return []
    return c.table("careers").select("code,name").eq("active", True).order("name").execute().data or []


def get_courses_for_career(career_code):
    if DEMO_MODE:
        return []
    c=_client()
    if not c or not career_code: return []
    rel = c.table("career_courses").select("course_code").eq("career_code", career_code).eq("is_egp_required", True).execute().data or []
    codes=[r["course_code"] for r in rel]
    if not codes: return []
    courses=c.table("courses").select("code,name,semester,area_id").in_("code",codes).eq("active",True).execute().data or []
    areas=c.table("egp_areas").select("id,name").execute().data or []
    amap={a["id"]:a["name"] for a in areas}
    for row in courses:
        row["area"] = amap.get(row.get("area_id"), "Sin área")
    return sorted(courses, key=lambda x:(x.get("area") or "", x.get("semester") or 99, x.get("name") or ""))


def get_areas_for_career(career_code):
    return sorted({r["area"] for r in get_courses_for_career(career_code)})


def get_all_courses():
    if DEMO_MODE: return []
    c=_client()
    if not c: return []
    courses=c.table("courses").select("code,name,semester,area_id,active").order("code").execute().data or []
    areas=c.table("egp_areas").select("id,name").execute().data or []
    amap={a["id"]:a["name"] for a in areas}
    for r in courses: r["area"]=amap.get(r.get("area_id"),"Sin área")
    return courses


def get_programs(include_drafts=False):
    if DEMO_MODE: return []
    c=_client()
    if not c: return []
    q=c.table("course_programs").select("id,course_code,version_label,effective_year,source_note,status,created_at")
    if not include_drafts:
        q=q.eq("status","publicado")
    return q.order("course_code").execute().data or []


def get_topics_for_program(program_id, include_drafts=False):
    if DEMO_MODE: return []
    c=_client()
    if not c or not program_id: return []
    q=c.table("topics").select("id,course_program_id,parent_id,title,sort_order,body_md,status").eq("course_program_id",program_id)
    if not include_drafts:
        q=q.eq("status","publicado")
    return q.order("sort_order").execute().data or []


def get_questions_for_career(career_code):
    if DEMO_MODE: return DEMO_QUESTIONS
    c=_client()
    if not c or not career_code: return []
    links=_fetch_all_pages(lambda: c.table("question_careers").select("question_id").eq("career_code",career_code), order_column="question_id")
    ids=[x["question_id"] for x in links]
    if not ids: return []
    return _fetch_questions_by_ids(c, ids, "id,area_id,course_code,topic_id,question_text,expected_answer,difficulty,competency,question_type,status", published_only=True)


CONTENT_STATUSES = ["borrador","en_revision","aprobado","publicado","archivado"]


def get_program(program_id):
    if DEMO_MODE: return None
    c=_client()
    if not c or not program_id: return None
    rows=(c.table("course_programs")
          .select("id,course_code,version_label,effective_year,source_note,status,created_by,created_at")
          .eq("id",program_id).limit(1).execute().data or [])
    return rows[0] if rows else None


def update_program_status(program_id, new_status):
    if DEMO_MODE: return False, "Disponible únicamente con Supabase."
    if new_status not in CONTENT_STATUSES:
        return False, "Estado no válido."
    c=_client()
    if not c: return False, "No hay conexión autenticada con Supabase."
    try:
        res=(c.table("course_programs")
             .update({"status":new_status})
             .eq("id",program_id).execute())
        if not res.data:
            return False, "Supabase no autorizó el cambio o no encontró el programa."
        return True, "Estado actualizado."
    except Exception as e:
        return False, f"No fue posible actualizar el estado: {e}"


def update_program_metadata(program_id, version_label, effective_year, source_note):
    if DEMO_MODE: return False, "Disponible únicamente con Supabase."
    c=_client()
    if not c: return False, "No hay conexión autenticada con Supabase."
    payload={
        "version_label": (version_label or "").strip(),
        "effective_year": int(effective_year) if effective_year else None,
        "source_note": (source_note or "").strip() or None,
    }
    try:
        res=c.table("course_programs").update(payload).eq("id",program_id).execute()
        if not res.data: return False, "No se pudo actualizar el programa."
        return True, "Programa actualizado."
    except Exception as e:
        return False, f"No fue posible actualizar el programa: {e}"


def add_topic(program_id, title, sort_order, body_md="", status="borrador"):
    if DEMO_MODE: return False, "Disponible únicamente con Supabase."
    c=_client()
    if not c: return False, "No hay conexión autenticada con Supabase."
    payload={
        "course_program_id": program_id,
        "parent_id": None,
        "title": (title or "").strip(),
        "sort_order": int(sort_order or 0),
        "body_md": body_md or None,
        "status": status,
    }
    if not payload["title"]: return False, "El título es obligatorio."
    try:
        res=c.table("topics").insert(payload).execute()
        if not res.data: return False, "No se pudo crear la unidad/tema."
        return True, "Unidad/tema creado."
    except Exception as e:
        return False, f"No fue posible crear la unidad/tema: {e}"


def update_topic(topic_id, title, sort_order, body_md, status):
    if DEMO_MODE: return False, "Disponible únicamente con Supabase."
    if status not in CONTENT_STATUSES: return False, "Estado no válido."
    c=_client()
    if not c: return False, "No hay conexión autenticada con Supabase."
    payload={
        "title": (title or "").strip(),
        "sort_order": int(sort_order or 0),
        "body_md": body_md or None,
        "status": status,
    }
    if not payload["title"]: return False, "El título es obligatorio."
    try:
        res=c.table("topics").update(payload).eq("id",topic_id).execute()
        if not res.data: return False, "No se pudo actualizar la unidad/tema."
        return True, "Unidad/tema actualizado."
    except Exception as e:
        return False, f"No fue posible actualizar la unidad/tema: {e}"


def delete_topic(topic_id):
    if DEMO_MODE: return False, "Disponible únicamente con Supabase."
    c=_client()
    if not c: return False, "No hay conexión autenticada con Supabase."
    try:
        c.table("topics").delete().eq("id",topic_id).execute()
        return True, "Unidad/tema eliminado."
    except Exception as e:
        return False, f"No fue posible eliminar la unidad/tema: {e}"


# ============================================================
# PREP-EIME v1.4 | BANCO DE PREGUNTAS
# ============================================================

QUESTION_TYPES = [
    "Respuesta abierta",
    "Problema de cálculo",
    "Análisis de caso",
    "Diseño / selección",
    "Defensa oral",
]

COMPETENCIES = [
    "Recordar",
    "Explicar",
    "Calcular",
    "Analizar",
    "Diseñar/Seleccionar",
    "Defender técnicamente",
]


def get_all_areas():
    if DEMO_MODE:
        return []
    c = _client()
    if not c:
        return []
    return c.table("egp_areas").select("id,name,description,active").eq("active", True).order("name").execute().data or []


def get_course_careers(course_code):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not course_code:
        return []
    rows = (
        c.table("career_courses")
        .select("career_code")
        .eq("course_code", course_code)
        .eq("is_egp_required", True)
        .execute().data or []
    )
    return sorted([r["career_code"] for r in rows])


def get_programs_for_course(course_code, include_drafts=True):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not course_code:
        return []
    q = (
        c.table("course_programs")
        .select("id,course_code,version_label,effective_year,source_note,status,created_at")
        .eq("course_code", course_code)
    )
    if not include_drafts:
        q = q.eq("status", "publicado")
    return q.order("effective_year", desc=True).execute().data or []


def get_topics_for_course(course_code, include_drafts=True):
    programs = get_programs_for_course(course_code, include_drafts=include_drafts)
    if not programs:
        return []
    rows = []
    for p in programs:
        for t in get_topics_for_program(p["id"], include_drafts=include_drafts):
            t = dict(t)
            t["program_version"] = p.get("version_label")
            t["program_status"] = p.get("status")
            rows.append(t)
    return sorted(rows, key=lambda x: (x.get("sort_order") or 0, x.get("title") or ""))


def get_all_questions(include_drafts=True):
    if DEMO_MODE:
        return []
    c = _client()
    if not c:
        return []

    q = c.table("questions").select(
        "id,area_id,course_code,topic_id,question_text,expected_answer,"
        "difficulty,competency,question_type,status,created_by,created_at"
    )
    if not include_drafts:
        q = q.eq("status", "publicado")

    questions = _fetch_all_pages(
        lambda: c.table("questions").select(
            "id,area_id,course_code,topic_id,question_text,expected_answer,"
            "difficulty,competency,question_type,status,created_by,created_at"
        ).eq("status", "publicado") if not include_drafts else c.table("questions").select(
            "id,area_id,course_code,topic_id,question_text,expected_answer,"
            "difficulty,competency,question_type,status,created_by,created_at"
        )
    )
    if not questions:
        return []

    links = _fetch_all_pages(lambda: c.table("question_careers").select("question_id,career_code"), order_column="question_id")
    cmap = {}
    for link in links:
        cmap.setdefault(link["question_id"], []).append(link["career_code"])

    for row in questions:
        row["careers"] = sorted(cmap.get(row["id"], []))
    return questions


def get_question(question_id):
    if DEMO_MODE:
        return None
    c = _client()
    if not c or not question_id:
        return None
    rows = (
        c.table("questions")
        .select(
            "id,area_id,course_code,topic_id,question_text,expected_answer,"
            "difficulty,competency,question_type,status,created_by,created_at"
        )
        .eq("id", question_id)
        .limit(1)
        .execute().data or []
    )
    if not rows:
        return None
    row = rows[0]
    links = (
        c.table("question_careers")
        .select("career_code")
        .eq("question_id", question_id)
        .execute().data or []
    )
    row["careers"] = sorted([x["career_code"] for x in links])
    return row


def _sync_question_careers(client, question_id, career_codes):
    career_codes = sorted(set(career_codes or []))
    existing = (
        client.table("question_careers")
        .select("career_code")
        .eq("question_id", question_id)
        .execute().data or []
    )
    existing_codes = {x["career_code"] for x in existing}
    target = set(career_codes)

    for code in existing_codes - target:
        client.table("question_careers").delete().eq("question_id", question_id).eq("career_code", code).execute()

    to_add = target - existing_codes
    if to_add:
        client.table("question_careers").insert([
            {"question_id": question_id, "career_code": code}
            for code in sorted(to_add)
        ]).execute()


def create_question(
    area_id,
    course_code,
    topic_id,
    question_text,
    expected_answer,
    difficulty,
    competency,
    question_type,
    career_codes,
    created_by,
):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase.", None
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase.", None

    question_text = (question_text or "").strip()
    expected_answer = (expected_answer or "").strip()
    if not question_text:
        return False, "La pregunta es obligatoria.", None
    if not career_codes:
        return False, "Selecciona al menos una carrera.", None

    payload = {
        "area_id": area_id or None,
        "course_code": course_code or None,
        "topic_id": topic_id or None,
        "question_text": question_text,
        "expected_answer": expected_answer or None,
        "difficulty": int(difficulty),
        "competency": competency or None,
        "question_type": question_type or None,
        "status": "borrador",
        "created_by": created_by,
    }

    try:
        res = c.table("questions").insert(payload).execute()
        if not res.data:
            return False, "No fue posible crear la pregunta.", None
        qid = res.data[0]["id"]
        _sync_question_careers(c, qid, career_codes)
        return True, "Pregunta creada como borrador.", qid
    except Exception as e:
        return False, f"No fue posible crear la pregunta: {e}", None


def update_question(
    question_id,
    area_id,
    course_code,
    topic_id,
    question_text,
    expected_answer,
    difficulty,
    competency,
    question_type,
    status,
    career_codes,
):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    if status not in CONTENT_STATUSES:
        return False, "Estado no válido."
    if not (question_text or "").strip():
        return False, "La pregunta es obligatoria."
    if not career_codes:
        return False, "Selecciona al menos una carrera."

    payload = {
        "area_id": area_id or None,
        "course_code": course_code or None,
        "topic_id": topic_id or None,
        "question_text": question_text.strip(),
        "expected_answer": (expected_answer or "").strip() or None,
        "difficulty": int(difficulty),
        "competency": competency or None,
        "question_type": question_type or None,
        "status": status,
    }

    try:
        res = c.table("questions").update(payload).eq("id", question_id).execute()
        if not res.data:
            return False, "No se pudo actualizar la pregunta."
        _sync_question_careers(c, question_id, career_codes)
        return True, "Pregunta actualizada."
    except Exception as e:
        return False, f"No fue posible actualizar la pregunta: {e}"


def update_question_status(question_id, new_status):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    if new_status not in CONTENT_STATUSES:
        return False, "Estado no válido."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        res = c.table("questions").update({"status": new_status}).eq("id", question_id).execute()
        if not res.data:
            return False, "No se pudo cambiar el estado."
        return True, "Estado de la pregunta actualizado."
    except Exception as e:
        return False, f"No fue posible cambiar el estado: {e}"


def delete_question(question_id):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        c.table("questions").delete().eq("id", question_id).execute()
        return True, "Pregunta eliminada."
    except Exception as e:
        return False, f"No fue posible eliminar la pregunta: {e}"


# ============================================================
# PREP-EIME v1.5 | SIMULADOR EGP
# ============================================================

import random
from datetime import datetime, timezone


def get_published_questions_for_simulator(career_code):
    """Preguntas publicadas asociadas a la carrera."""
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not career_code:
        return []

    links = _fetch_all_pages(
        lambda: c.table("question_careers").select("question_id").eq("career_code", career_code),
        order_column="question_id",
    )
    ids = [x["question_id"] for x in links]
    if not ids:
        return []

    rows = _fetch_questions_by_ids(
        c, ids,
        "id,area_id,course_code,topic_id,question_text,expected_answer,"
        "difficulty,competency,question_type,status",
        published_only=True,
    )
    return rows


def build_simulator_question_set(
    career_code,
    question_count=10,
    area_names=None,
    difficulty_levels=None,
):
    """Construye una muestra aleatoria, respetando filtros disponibles."""
    questions = get_published_questions_for_simulator(career_code)
    if not questions:
        return []

    courses = {c["code"]: c for c in get_courses_for_career(career_code)}

    filtered = []
    for q in questions:
        course = courses.get(q.get("course_code"), {})
        area = course.get("area")
        if area_names and area not in area_names:
            continue
        if difficulty_levels and q.get("difficulty") not in difficulty_levels:
            continue
        q = dict(q)
        q["area"] = area or "Sin área"
        q["course_name"] = course.get("name") or q.get("course_code")
        filtered.append(q)

    # Distribución equilibrada entre áreas con preguntas elegibles.
    # En cada ronda se toma como máximo una pregunta por área; cuando
    # alguna se agota, las restantes siguen cubriendo los cupos.
    area_pools = {}
    for row in filtered:
        area_pools.setdefault(row["area"], []).append(row)
    for pool in area_pools.values():
        random.shuffle(pool)

    areas = list(area_pools)
    random.shuffle(areas)  # Desempate aleatorio si hay menos cupos que áreas.
    limit = min(max(0, int(question_count)), len(filtered))
    selected = []
    while len(selected) < limit:
        available = [area for area in areas if area_pools[area]]
        if not available:
            break
        random.shuffle(available)  # Distribuye equitativamente los sobrantes.
        for area in available:
            if len(selected) >= limit:
                break
            selected.append(area_pools[area].pop())
    random.shuffle(selected)  # No agrupar las preguntas por área al mostrarlas.
    return selected


def create_attempt(student_id, career_code, question_ids, duration_minutes=60):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase.", None
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase.", None
    if not question_ids:
        return False, "No hay preguntas para iniciar el simulacro.", None

    payload = {
        "student_id": student_id,
        "attempt_type": "simulador_escrito",
        "career_code": career_code,
        "status": "en_progreso",
        "duration_minutes": int(duration_minutes),
        "question_count": len(question_ids),
        "metadata": {
            "question_ids": question_ids,
            "version": "v1.5",
            "evaluation_mode": "autoevaluacion_guiada",
        },
    }

    try:
        res = c.table("attempts").insert(payload).execute()
        if not res.data:
            return False, "No se pudo crear el intento.", None
        attempt_id = res.data[0]["id"]

        c.table("attempt_answers").insert([
            {
                "attempt_id": attempt_id,
                "question_id": qid,
                "answer_text": None,
                "score": None,
                "self_score": None,
                "evaluation_status": "pendiente",
            }
            for qid in question_ids
        ]).execute()

        return True, "Simulacro iniciado.", attempt_id
    except Exception as e:
        return False, f"No fue posible iniciar el simulacro: {e}", None


def get_attempt(attempt_id):
    if DEMO_MODE:
        return None
    c = _client()
    if not c or not attempt_id:
        return None
    rows = (
        c.table("attempts")
        .select(
            "id,student_id,attempt_type,career_code,started_at,finished_at,"
            "score,status,duration_minutes,question_count,metadata,"
            "grading_mode,grading_status,published_at"
        )
        .eq("id", attempt_id)
        .limit(1)
        .execute().data or []
    )
    return rows[0] if rows else None


def get_attempt_answers(attempt_id):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not attempt_id:
        return []

    answers = (
        c.table("attempt_answers")
        .select(
            "id,attempt_id,question_id,answer_text,score,feedback,"
            "self_score,evaluation_status,answered_at"
        )
        .eq("attempt_id", attempt_id)
        .execute().data or []
    )
    if not answers:
        return []

    qids = [a["question_id"] for a in answers]
    questions = (
        c.table("questions")
        .select(
            "id,area_id,course_code,topic_id,question_text,expected_answer,"
            "difficulty,competency,question_type"
        )
        .in_("id", qids)
        .execute().data or []
    )
    qmap = {q["id"]: q for q in questions}

    attempt = get_attempt(attempt_id)
    career = attempt.get("career_code") if attempt else None
    courses = {
        x["code"]: x for x in get_courses_for_career(career)
    } if career else {}

    order = []
    if attempt:
        order = (attempt.get("metadata") or {}).get("question_ids", [])

    order_map = {qid: i for i, qid in enumerate(order)}

    out = []
    for a in answers:
        row = dict(a)
        q = qmap.get(a["question_id"], {})
        row.update({
            "question_text": q.get("question_text"),
            "expected_answer": q.get("expected_answer"),
            "difficulty": q.get("difficulty"),
            "competency": q.get("competency"),
            "question_type": q.get("question_type"),
            "course_code": q.get("course_code"),
            "area_id": q.get("area_id"),
            "topic_id": q.get("topic_id"),
        })
        course = courses.get(q.get("course_code"), {})
        row["course_name"] = course.get("name") or q.get("course_code")
        row["area"] = course.get("area") or "Sin área"
        out.append(row)

    return sorted(out, key=lambda x: order_map.get(x["question_id"], 999999))


def save_attempt_answer(answer_id, answer_text):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        res = (
            c.table("attempt_answers")
            .update({
                "answer_text": answer_text or None,
                "answered_at": datetime.now(timezone.utc).isoformat(),
            })
            .eq("id", answer_id)
            .execute()
        )
        if not res.data:
            return False, "No fue posible guardar la respuesta."
        return True, "Respuesta guardada."
    except Exception as e:
        return False, f"No fue posible guardar la respuesta: {e}"


def finish_attempt(attempt_id):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        res = (
            c.table("attempts")
            .update({
                "status": "finalizado",
                "finished_at": datetime.now(timezone.utc).isoformat(),
            })
            .eq("id", attempt_id)
            .execute()
        )
        if not res.data:
            return False, "No fue posible finalizar el intento."
        return True, "Simulacro finalizado. Ahora realiza la autoevaluación guiada."
    except Exception as e:
        return False, f"No fue posible finalizar el intento: {e}"


def save_self_evaluation(answer_id, self_score, feedback=None):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        score = float(self_score)
        res = (
            c.table("attempt_answers")
            .update({
                "self_score": score,
                "score": score,
                "feedback": feedback or None,
                "evaluation_status": "autoevaluado",
            })
            .eq("id", answer_id)
            .execute()
        )
        if not res.data:
            return False, "No se pudo registrar la autoevaluación."
        return True, "Autoevaluación registrada."
    except Exception as e:
        return False, f"No fue posible guardar la autoevaluación: {e}"


def recompute_attempt_score(attempt_id):
    if DEMO_MODE:
        return None
    c = _client()
    if not c:
        return None

    answers = get_attempt_answers(attempt_id)
    scored = [
        float(a["score"])
        for a in answers
        if a.get("score") is not None
    ]
    final_score = round(sum(scored) / len(scored), 2) if scored else None

    try:
        c.table("attempts").update({"score": final_score}).eq("id", attempt_id).execute()
    except Exception:
        pass
    return final_score


def get_student_attempts(student_id):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not student_id:
        return []
    return (
        c.table("attempts")
        .select(
            "id,attempt_type,career_code,started_at,finished_at,score,status,"
            "duration_minutes,question_count,metadata"
        )
        .eq("student_id", student_id)
        .order("started_at", desc=True)
        .execute().data or []
    )


def get_attempt_diagnostics(attempt_id):
    answers = get_attempt_answers(attempt_id)
    if not answers:
        return {
            "overall": None,
            "by_area": [],
            "by_course": [],
            "by_competency": [],
            "by_difficulty": [],
            "evaluated": 0,
            "total": 0,
        }

    evaluated = [a for a in answers if a.get("score") is not None]

    def aggregate(key):
        groups = {}
        for a in evaluated:
            label = a.get(key)
            if label is None:
                label = "Sin clasificar"
            groups.setdefault(str(label), []).append(float(a["score"]))
        return [
            {"label": label, "score": round(sum(vals) / len(vals), 2), "n": len(vals)}
            for label, vals in sorted(groups.items())
        ]

    overall = (
        round(sum(float(a["score"]) for a in evaluated) / len(evaluated), 2)
        if evaluated else None
    )

    return {
        "overall": overall,
        "by_area": aggregate("area"),
        "by_course": aggregate("course_name"),
        "by_competency": aggregate("competency"),
        "by_difficulty": aggregate("difficulty"),
        "evaluated": len(evaluated),
        "total": len(answers),
    }


# ============================================================
# PREP-EIME v1.6 | EVALUACIÓN ESTRUCTURADA
# ============================================================

EVALUATION_MODES = {
    "autocalificable": "Autocalificable",
    "autoevaluacion": "Autoevaluación guiada",
    "rubrica": "Rúbrica / revisión",
}

STRUCTURED_QUESTION_TYPES = [
    "Opción múltiple",
    "Respuesta numérica",
    "Respuesta abierta",
    "Problema de cálculo",
    "Análisis de caso",
    "Diseño / selección",
    "Defensa oral",
]


def _question_select_v16():
    return (
        "id,area_id,course_code,topic_id,question_text,expected_answer,"
        "difficulty,competency,question_type,status,created_by,created_at,"
        "evaluation_mode,answer_config,rubric,weight"
    )


def get_all_questions_v16(include_drafts=True):
    if DEMO_MODE:
        return []
    c = _client()
    if not c:
        return []

    q = c.table("questions").select(_question_select_v16())
    if not include_drafts:
        q = q.eq("status", "publicado")

    questions = _fetch_all_pages(
        lambda: c.table("questions").select(_question_select_v16()).eq("status", "publicado")
        if not include_drafts else c.table("questions").select(_question_select_v16())
    )
    links = _fetch_all_pages(lambda: c.table("question_careers").select("question_id,career_code"), order_column="question_id")

    cmap = {}
    for link in links:
        cmap.setdefault(link["question_id"], []).append(link["career_code"])

    for row in questions:
        row["careers"] = sorted(cmap.get(row["id"], []))
        row["answer_config"] = row.get("answer_config") or {}
        row["rubric"] = row.get("rubric") or []
    return questions


def get_published_questions_for_simulator_v16(career_code):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not career_code:
        return []

    links = _fetch_all_pages(
        lambda: c.table("question_careers").select("question_id").eq("career_code", career_code),
        order_column="question_id",
    )
    ids = [x["question_id"] for x in links]
    if not ids:
        return []

    rows = _fetch_questions_by_ids(c, ids, _question_select_v16(), published_only=True)
    for row in rows:
        row["answer_config"] = row.get("answer_config") or {}
        row["rubric"] = row.get("rubric") or []
    return rows


def create_question_v16(
    area_id, course_code, topic_id, question_text, expected_answer,
    difficulty, competency, question_type, career_codes, created_by,
    evaluation_mode="autoevaluacion", answer_config=None, rubric=None, weight=1.0
):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase.", None
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase.", None
    if not (question_text or "").strip():
        return False, "La pregunta es obligatoria.", None
    if not career_codes:
        return False, "Selecciona al menos una carrera.", None

    payload = {
        "area_id": area_id or None,
        "course_code": course_code or None,
        "topic_id": topic_id or None,
        "question_text": question_text.strip(),
        "expected_answer": (expected_answer or "").strip() or None,
        "difficulty": int(difficulty),
        "competency": competency or None,
        "question_type": question_type or None,
        "status": "borrador",
        "created_by": created_by,
        "evaluation_mode": evaluation_mode,
        "answer_config": answer_config or {},
        "rubric": rubric or [],
        "weight": float(weight or 1.0),
    }

    try:
        res = c.table("questions").insert(payload).execute()
        if not res.data:
            return False, "No fue posible crear la pregunta.", None
        qid = res.data[0]["id"]
        _sync_question_careers(c, qid, career_codes)
        return True, "Pregunta creada como borrador.", qid
    except Exception as e:
        return False, f"No fue posible crear la pregunta: {e}", None


def update_question_v16(
    question_id, area_id, course_code, topic_id, question_text, expected_answer,
    difficulty, competency, question_type, status, career_codes,
    evaluation_mode="autoevaluacion", answer_config=None, rubric=None, weight=1.0
):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    if not (question_text or "").strip():
        return False, "La pregunta es obligatoria."
    if not career_codes:
        return False, "Selecciona al menos una carrera."

    payload = {
        "area_id": area_id or None,
        "course_code": course_code or None,
        "topic_id": topic_id or None,
        "question_text": question_text.strip(),
        "expected_answer": (expected_answer or "").strip() or None,
        "difficulty": int(difficulty),
        "competency": competency or None,
        "question_type": question_type or None,
        "status": status,
        "evaluation_mode": evaluation_mode,
        "answer_config": answer_config or {},
        "rubric": rubric or [],
        "weight": float(weight or 1.0),
    }

    try:
        res = c.table("questions").update(payload).eq("id", question_id).execute()
        if not res.data:
            return False, "No se pudo actualizar la pregunta."
        _sync_question_careers(c, question_id, career_codes)
        return True, "Pregunta actualizada."
    except Exception as e:
        return False, f"No fue posible actualizar la pregunta: {e}"


def build_simulator_question_set_v16(
    career_code, question_count=10, area_names=None, difficulty_levels=None
):
    questions = get_published_questions_for_simulator_v16(career_code)
    if not questions:
        return []

    courses = {c["code"]: c for c in get_courses_for_career(career_code)}
    filtered = []

    for q in questions:
        course = courses.get(q.get("course_code"), {})
        area = course.get("area")
        if area_names and area not in area_names:
            continue
        if difficulty_levels and q.get("difficulty") not in difficulty_levels:
            continue
        row = dict(q)
        row["area"] = area or "Sin área"
        row["course_name"] = course.get("name") or q.get("course_code")
        filtered.append(row)

    # Distribución equilibrada entre áreas con preguntas elegibles.
    # En cada ronda se toma como máximo una pregunta por área; cuando
    # alguna se agota, las restantes siguen cubriendo los cupos.
    area_pools = {}
    for row in filtered:
        area_pools.setdefault(row["area"], []).append(row)
    for pool in area_pools.values():
        random.shuffle(pool)

    areas = list(area_pools)
    random.shuffle(areas)  # Desempate aleatorio si hay menos cupos que áreas.
    limit = min(max(0, int(question_count)), len(filtered))
    selected = []
    while len(selected) < limit:
        available = [area for area in areas if area_pools[area]]
        if not available:
            break
        random.shuffle(available)  # Distribuye equitativamente los sobrantes.
        for area in available:
            if len(selected) >= limit:
                break
            selected.append(area_pools[area].pop())
    random.shuffle(selected)  # No agrupar las preguntas por área al mostrarlas.
    return selected


def get_attempt_answers_v16(attempt_id):
    if DEMO_MODE:
        return []
    c = _client()
    if not c or not attempt_id:
        return []

    answers = (
        c.table("attempt_answers")
        .select(
            "id,attempt_id,question_id,answer_text,score,feedback,self_score,"
            "evaluation_status,answered_at,auto_score,review_score,"
            "reviewed_by,reviewed_at"
        )
        .eq("attempt_id", attempt_id)
        .execute().data or []
    )
    if not answers:
        return []

    qids = [a["question_id"] for a in answers]
    questions = (
        c.table("questions")
        .select(_question_select_v16())
        .in_("id", qids)
        .execute().data or []
    )
    qmap = {q["id"]: q for q in questions}

    attempt = get_attempt(attempt_id)
    career = attempt.get("career_code") if attempt else None
    courses = {
        x["code"]: x for x in get_courses_for_career(career)
    } if career else {}

    order = (attempt.get("metadata") or {}).get("question_ids", []) if attempt else []
    order_map = {qid: i for i, qid in enumerate(order)}

    out = []
    for a in answers:
        row = dict(a)
        q = qmap.get(a["question_id"], {})
        row.update({
            "question_text": q.get("question_text"),
            "expected_answer": q.get("expected_answer"),
            "difficulty": q.get("difficulty"),
            "competency": q.get("competency"),
            "question_type": q.get("question_type"),
            "course_code": q.get("course_code"),
            "area_id": q.get("area_id"),
            "topic_id": q.get("topic_id"),
            "evaluation_mode": q.get("evaluation_mode") or "autoevaluacion",
            "answer_config": q.get("answer_config") or {},
            "rubric": q.get("rubric") or [],
            "weight": float(q.get("weight") or 1.0),
        })
        course = courses.get(q.get("course_code"), {})
        row["course_name"] = course.get("name") or q.get("course_code")
        row["area"] = course.get("area") or "Sin área"
        out.append(row)

    return sorted(out, key=lambda x: order_map.get(x["question_id"], 999999))


def auto_grade_answer(answer_id):
    """Califica opción múltiple o respuesta numérica. Devuelve (ok,msg,score)."""
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase.", None
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase.", None

    rows = (
        c.table("attempt_answers")
        .select("id,question_id,answer_text")
        .eq("id", answer_id)
        .limit(1)
        .execute().data or []
    )
    if not rows:
        return False, "Respuesta no encontrada.", None

    ans = rows[0]
    qrows = (
        c.table("questions")
        .select("question_type,evaluation_mode,answer_config")
        .eq("id", ans["question_id"])
        .limit(1)
        .execute().data or []
    )
    if not qrows:
        return False, "Pregunta no encontrada.", None

    q = qrows[0]
    if q.get("evaluation_mode") != "autocalificable":
        return False, "La pregunta no es autocalificable.", None

    cfg = q.get("answer_config") or {}
    raw = (ans.get("answer_text") or "").strip()
    score = 0.0
    feedback = None

    if q.get("question_type") == "Opción múltiple":
        correct = str(cfg.get("correct_option", "")).strip()
        score = 100.0 if raw == correct and correct != "" else 0.0
        feedback = "Respuesta correcta." if score == 100 else "Respuesta incorrecta."

    elif q.get("question_type") == "Respuesta numérica":
        try:
            submitted = float(raw.replace(",", "."))
            correct = float(cfg.get("correct_value"))
            tolerance = abs(float(cfg.get("tolerance", 0)))
            error = abs(submitted - correct)
            score = 100.0 if error <= tolerance else 0.0
            feedback = (
                f"Dentro de la tolerancia ±{tolerance:g}."
                if score == 100
                else f"Fuera de la tolerancia ±{tolerance:g}."
            )
        except Exception:
            score = 0.0
            feedback = "No fue posible interpretar la respuesta como un valor numérico."
    else:
        return False, "Tipo autocalificable no reconocido.", None

    try:
        c.table("attempt_answers").update({
            "auto_score": score,
            "score": score,
            "feedback": feedback,
            "evaluation_status": "revisado",
        }).eq("id", answer_id).execute()
        return True, feedback, score
    except Exception as e:
        return False, f"No fue posible guardar la calificación: {e}", None


def finalize_autograded_answers(attempt_id):
    answers = get_attempt_answers_v16(attempt_id)
    results = []
    for a in answers:
        if a.get("evaluation_mode") == "autocalificable":
            ok, msg, score = auto_grade_answer(a["id"])
            results.append((a["id"], ok, score))
    recompute_attempt_score_v16(attempt_id)
    return results


def save_self_evaluation_v16(answer_id, self_score, feedback=None):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        score = float(self_score)
        c.table("attempt_answers").update({
            "self_score": score,
            "score": score,
            "feedback": feedback or None,
            "evaluation_status": "autoevaluado",
        }).eq("id", answer_id).execute()
        return True, "Autoevaluación registrada."
    except Exception as e:
        return False, f"No fue posible guardar la autoevaluación: {e}"


def review_answer_with_rubric(answer_id, review_score, feedback, reviewer_id):
    if DEMO_MODE:
        return False, "Disponible únicamente con Supabase."
    c = _client()
    if not c:
        return False, "No hay conexión autenticada con Supabase."
    try:
        score = float(review_score)
        c.table("attempt_answers").update({
            "review_score": score,
            "score": score,
            "feedback": feedback or None,
            "reviewed_by": reviewer_id,
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            "evaluation_status": "revisado",
        }).eq("id", answer_id).execute()
        return True, "Revisión docente guardada."
    except Exception as e:
        return False, f"No fue posible guardar la revisión: {e}"


def recompute_attempt_score_v16(attempt_id):
    if DEMO_MODE:
        return None
    c = _client()
    if not c:
        return None

    answers = get_attempt_answers_v16(attempt_id)
    scored = [a for a in answers if a.get("score") is not None]
    if not scored:
        final_score = None
    else:
        weighted_sum = sum(float(a["score"]) * float(a.get("weight") or 1) for a in scored)
        total_weight = sum(float(a.get("weight") or 1) for a in scored)
        final_score = round(weighted_sum / total_weight, 2) if total_weight else None

    try:
        c.table("attempts").update({"score": final_score}).eq("id", attempt_id).execute()
    except Exception:
        pass
    return final_score


def get_attempt_diagnostics_v16(attempt_id):
    answers = get_attempt_answers_v16(attempt_id)
    if not answers:
        return {
            "overall": None, "by_area": [], "by_course": [],
            "by_competency": [], "by_difficulty": [],
            "evaluated": 0, "total": 0, "pending_review": 0
        }

    evaluated = [a for a in answers if a.get("score") is not None]

    def aggregate(key):
        groups = {}
        for a in evaluated:
            label = a.get(key)
            if label is None:
                label = "Sin clasificar"
            groups.setdefault(str(label), []).append(
                (float(a["score"]), float(a.get("weight") or 1))
            )
        out = []
        for label, vals in sorted(groups.items()):
            num = sum(s*w for s, w in vals)
            den = sum(w for _, w in vals)
            out.append({
                "label": label,
                "score": round(num/den, 2) if den else 0,
                "n": len(vals)
            })
        return out

    if evaluated:
        num = sum(float(a["score"]) * float(a.get("weight") or 1) for a in evaluated)
        den = sum(float(a.get("weight") or 1) for a in evaluated)
        overall = round(num / den, 2) if den else None
    else:
        overall = None

    pending_review = sum(
        1 for a in answers
        if a.get("evaluation_mode") == "rubrica"
        and a.get("evaluation_status") != "revisado"
    )

    return {
        "overall": overall,
        "by_area": aggregate("area"),
        "by_course": aggregate("course_name"),
        "by_competency": aggregate("competency"),
        "by_difficulty": aggregate("difficulty"),
        "evaluated": len(evaluated),
        "total": len(answers),
        "pending_review": pending_review,
    }


def get_staff_attempts(limit=100):
    if DEMO_MODE:
        return []
    c = _client()
    if not c:
        return []
    return (
        c.table("attempts")
        .select(
            "id,student_id,attempt_type,career_code,started_at,finished_at,"
            "score,status,duration_minutes,question_count,metadata"
        )
        .eq("status", "finalizado")
        .order("started_at", desc=True)
        .limit(limit)
        .execute().data or []
    )


def get_profiles_by_ids(ids):
    if DEMO_MODE or not ids:
        return {}
    c = _client()
    if not c:
        return {}
    rows = (
        c.table("profiles")
        .select("id,full_name,student_id,career_code")
        .in_("id", list(set(ids)))
        .execute().data or []
    )
    return {r["id"]: r for r in rows}

# v1.7
from datetime import datetime, timezone

def get_quality_reviews():
    c=_client()
    if not c: return {}
    return {r['question_id']: r for r in _fetch_all_pages(lambda: c.table('question_quality_reviews').select('*'), order_column='question_id')}

def save_quality_review(question_id, reviewer_id, checks, notes):
    c=_client()
    if not c: return False,'Sin sesión.'
    payload={'question_id':question_id,'reviewer_id':reviewer_id,'reviewed_at':datetime.now(timezone.utc).isoformat(),'notes':notes}
    for k in ('clarity','topic_alignment','technical_accuracy','answer_quality','evaluation_quality'):
        payload[k]=bool(checks.get(k))
    try:
        c.table('question_quality_reviews').upsert(payload,on_conflict='question_id').execute()
        return True,'Revisión registrada.'
    except Exception as e: return False,str(e)

def bulk_transition_questions(ids,target):
    c=_client()
    if not c or not ids: return []
    return c.rpc('bulk_transition_reviewed_questions',{'p_question_ids':ids[:100],'p_target':target}).execute().data or []
