from .supabase_client import get_supabase_client


def pending_requests():
    client = get_supabase_client(require_auth=True)
    result = client.rpc("prep_pending_registrations").execute()
    return result.data or []


def decide_request(profile_id, approve):
    try:
        client = get_supabase_client(require_auth=True)
        result = client.rpc("prep_decide_registration", {"p_profile_id": profile_id, "p_approve": bool(approve)}).execute()
        if result.data is not True:
            return False, "No se pudo completar la decisión."
        return True, "Solicitud aprobada." if approve else "Solicitud rechazada."
    except Exception:
        return False, "No se pudo actualizar la solicitud. Comprueba los permisos de administrador."
