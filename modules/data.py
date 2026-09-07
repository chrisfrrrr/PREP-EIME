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
