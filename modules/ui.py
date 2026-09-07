
import streamlit as st

def apply_branding():
    st.markdown(
        '''
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1250px;}
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
