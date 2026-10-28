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
