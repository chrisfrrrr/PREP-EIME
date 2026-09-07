
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_setting(name: str, default: str = "") -> str:
    """
    Priority:
    1) Streamlit Community Cloud secrets
    2) Environment variables / local .env
    3) Default value
    """
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)

APP_NAME = get_setting("APP_NAME", "PREP-EIME")
DEMO_MODE = get_setting("DEMO_MODE", "true").lower() == "true"
SUPABASE_URL = get_setting("SUPABASE_URL", "")
SUPABASE_KEY = get_setting("SUPABASE_KEY", "")

def supabase_is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)
