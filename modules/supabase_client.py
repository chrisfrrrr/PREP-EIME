import streamlit as st
from supabase import create_client
from .config import SUPABASE_URL, SUPABASE_KEY, supabase_is_configured


def get_supabase_client(require_auth: bool = True):
    if not supabase_is_configured():
        return None
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    if require_auth:
        access = st.session_state.get("sb_access_token")
        refresh = st.session_state.get("sb_refresh_token")
        if access and refresh:
            try:
                client.auth.set_session(access, refresh)
            except Exception:
                return None
    return client
