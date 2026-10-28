from .supabase_client import get_supabase_client

def client():
    c = get_supabase_client(require_auth=True)
    if not c:
        raise RuntimeError("Se requiere una sesión Supabase autenticada")
    return c

def attempts():
    return (client().table("attempts").select("id,student_id,career_code,finished_at,grading_status")
        .eq("status","finalizado").eq("grading_mode","administrativa")
        .order("finished_at",desc=True).limit(200).execute().data or [])

def rubrics():
    return (client().table("grading_rubrics").select("id,code,name")
        .eq("is_active",True).order("code").execute().data or [])

def criteria(rubric_id):
    return (client().table("grading_criteria").select("criterion_order,name,max_points")
        .eq("rubric_id",rubric_id).order("criterion_order").execute().data or [])

def evaluation(answer_id):
    rows = (client().table("answer_rubric_evaluations").select("id,rubric_id,status,version")
        .eq("attempt_answer_id",answer_id).limit(1).execute().data or [])
    if not rows: return None, []
    scores=(client().table("answer_criterion_scores").select("criterion_order,performance_level")
        .eq("evaluation_id",rows[0]["id"]).execute().data or [])
    return rows[0], scores

def save(answer_id,code,items,version):
    return client().rpc("save_answer_rubric_evaluation",{
        "p_attempt_answer_id":answer_id,"p_rubric_code":code,
        "p_criteria":items,"p_expected_version":version}).execute().data


def progress(attempt_id):
    """Admin-only read of grading progress; no publication side effects."""
    c=client()
    answers=(c.table("attempt_answers").select("id").eq("attempt_id",attempt_id).execute().data or [])
    ids=[a["id"] for a in answers]
    evaluations=[]
    if ids:
        evaluations=(c.table("answer_rubric_evaluations")
            .select("attempt_answer_id,status,version")
            .in_("attempt_answer_id",ids).execute().data or [])
    by_answer={e["attempt_answer_id"]:e for e in evaluations}
    complete=sum(by_answer.get(i,{}).get("status")=="completa" for i in ids)
    drafts=sum(by_answer.get(i,{}).get("status")=="borrador" for i in ids)
    return {"total":len(ids),"completas":complete,"borradores":drafts,
        "pendientes":len(ids)-complete-drafts,
        "porcentaje":100.0*complete/len(ids) if ids else 0.0,
        "por_respuesta":by_answer}


def publication_preview(attempt_id):
    """Compute an administrator-only preview without changing the database."""
    state=progress(attempt_id)
    if not state["total"] or state["completas"]!=state["total"]:
        return {**state,"ready":False,"score":None}
    ids=list(state["por_respuesta"])
    eval_ids=[]
    for answer_id in ids:
        row=(client().table("answer_rubric_evaluations")
            .select("id,status").eq("attempt_answer_id",answer_id).single().execute().data)
        if not row or row["status"]!="completa":
            return {**state,"ready":False,"score":None}
        eval_ids.append(row["id"])
    rows=(client().table("answer_criterion_scores")
        .select("evaluation_id,awarded_points")
        .in_("evaluation_id",eval_ids).execute().data or [])
    totals={eid:[] for eid in eval_ids}
    for row in rows:
        if row["evaluation_id"] in totals:
            totals[row["evaluation_id"]].append(float(row["awarded_points"]))
    if any(len(points)!=5 for points in totals.values()):
        return {**state,"ready":False,"score":None}
    return {**state,"ready":True,
            "score":round(sum(sum(points) for points in totals.values())/len(totals),2)}


def publish(attempt_id):
    """Always relies on Supabase's administrator-only authorization."""
    return client().rpc("publish_attempt_grades",{"p_attempt_id":attempt_id}).execute().data


def publication_enabled():
    """Fail-closed switch. Enable only after the SQL security migration is tested."""
    import streamlit as st
    return st.secrets.get("ENABLE_ADMIN_PUBLICATION", False) is True


def published_result(attempt_id):
    """Server decides visibility; no client-side grade/status trust."""
    return client().rpc("get_my_published_attempt_result", {
        "p_attempt_id": attempt_id
    }).execute().data
