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
    links=c.table("question_careers").select("question_id").eq("career_code",career_code).execute().data or []
    ids=[x["question_id"] for x in links]
    if not ids: return []
    return c.table("questions").select("id,area_id,course_code,topic_id,question_text,expected_answer,difficulty,competency,question_type,status").in_("id",ids).eq("status","publicado").execute().data or []


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

    questions = q.order("created_at", desc=True).execute().data or []
    if not questions:
        return []

    links = c.table("question_careers").select("question_id,career_code").execute().data or []
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
