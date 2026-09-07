
import streamlit as st
from .config import DEMO_MODE, SUPABASE_URL, SUPABASE_KEY
from .data import DEMO_USERS

def _supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def login(email: str, password: str):
    email = email.strip().lower()

    if DEMO_MODE:
        user = DEMO_USERS.get(email)
        if user and user["password"] == password:
            return {k:v for k,v in user.items() if k != "password"} | {"email": email}
        return None

    client = _supabase_client()
    if client is None:
        return None

    auth = client.auth.sign_in_with_password({"email": email, "password": password})
    if not auth.user:
        return None

    profile = (
        client.table("profiles")
        .select("id,full_name,role,career_code,cohort_code,student_id,status")
        .eq("id", auth.user.id)
        .single()
        .execute()
    )
    if not profile.data:
        return None

    return {
        "email": email,
        "name": profile.data.get("full_name"),
        "role": profile.data.get("role"),
        "career_code": profile.data.get("career_code"),
        "cohort": profile.data.get("cohort_code"),
        "student_id": profile.data.get("student_id"),
        "status": profile.data.get("status"),
    }

def logout():
    st.session_state.pop("user", None)
    st.rerun()
