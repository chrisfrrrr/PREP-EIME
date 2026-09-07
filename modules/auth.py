import streamlit as st
from .config import DEMO_MODE, supabase_is_configured
from .data import DEMO_USERS
from .supabase_client import get_supabase_client


def login(email: str, password: str):
    email = email.strip().lower()

    if DEMO_MODE:
        user = DEMO_USERS.get(email)
        if user and user["password"] == password:
            return {k: v for k, v in user.items() if k != "password"} | {"email": email}
        return None

    if not supabase_is_configured():
        st.error("Supabase no está configurado. Revisa los Secrets de Streamlit.")
        return None

    try:
        client = get_supabase_client(require_auth=False)
        auth = client.auth.sign_in_with_password({"email": email, "password": password})
        if not auth.user or not auth.session:
            return None

        st.session_state.sb_access_token = auth.session.access_token
        st.session_state.sb_refresh_token = auth.session.refresh_token

        client = get_supabase_client(require_auth=True)
        profile = (
            client.table("profiles")
            .select("id,full_name,role,career_code,cohort_code,student_id,status")
            .eq("id", auth.user.id)
            .single()
            .execute()
        )
        if not profile.data:
            st.error("El usuario existe en autenticación, pero no tiene perfil en PREP-EIME.")
            return None
        if profile.data.get("status") != "activo":
            st.error("Este usuario no tiene acceso activo a PREP-EIME.")
            return None

        return {
            "id": str(auth.user.id),
            "email": email,
            "name": profile.data.get("full_name"),
            "role": profile.data.get("role"),
            "career_code": profile.data.get("career_code"),
            "cohort": profile.data.get("cohort_code"),
            "student_id": profile.data.get("student_id"),
            "status": profile.data.get("status"),
        }
    except Exception:
        st.session_state.pop("sb_access_token", None)
        st.session_state.pop("sb_refresh_token", None)
        st.error("No fue posible iniciar sesión. Verifica las credenciales y la configuración de Supabase.")
        return None


def logout():
    try:
        client = get_supabase_client(require_auth=True)
        if client:
            client.auth.sign_out()
    except Exception:
        pass
    for key in ("user", "sb_access_token", "sb_refresh_token"):
        st.session_state.pop(key, None)
    st.rerun()
