
import streamlit as st

def apply_branding():
    st.markdown(
        '''
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1250px;}
        .prep-login-heading {text-align:center;font-size:2.7rem;font-weight:850;letter-spacing:.02em;color:#0A355E;margin:1.3rem 0 .1rem;}
        .prep-login-sub {text-align:center;color:#5B6673;font-size:.95rem;margin-bottom:1.8rem;}
        div.stButton>button[kind="primary"],div.stFormSubmitButton>button[kind="primary"] {background:#0A355E;border-radius:9px;}
        [data-testid="stSidebar"] {border-right:4px solid #B28A39;}
        [data-testid="stSidebar"] {background: #0A355E;}
        [data-testid="stSidebar"] * {color: white;}
        .prep-card {
            background: white;
            border: 1px solid #DCE4EC;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 18px rgba(0,0,0,.05);
            min-height: 118px;
        }
        .prep-kpi {font-size: 1.85rem; font-weight: 750; color: #0B4F8A;}
        .prep-muted {color:#5B6673; font-size:.92rem;}
        .prep-title {font-size: 2rem; font-weight: 800; color:#14213D; margin-bottom:.25rem;}
        .prep-subtitle {color:#566573; margin-top:0;}
        .tag {
            display:inline-block; padding:4px 10px; border-radius:999px;
            background:#EAF0F6; color:#0B4F8A; font-size:.8rem; margin-right:6px;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

def page_header(title, subtitle=None):
    st.markdown(f'<div class="prep-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="prep-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def metric_card(title, value, foot=""):
    st.markdown(
        f'''<div class="prep-card">
        <div class="prep-muted">{title}</div>
        <div class="prep-kpi">{value}</div>
        <div class="prep-muted">{foot}</div>
        </div>''',
        unsafe_allow_html=True
    )
