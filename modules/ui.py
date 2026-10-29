"""Componentes de presentación livianos de PREP-EIME."""
from html import escape
import streamlit as st


def apply_branding():
    st.markdown("""<style>
    :root { --prep-navy:#0A355E; --prep-gold:#B28A39; }
    .block-container {max-width:1240px;padding-top:1.5rem;padding-bottom:3.5rem;}
    .prep-login-heading{text-align:center;font-size:clamp(2rem,4vw,2.7rem);font-weight:800;color:#0A355E;margin:1rem 0 .2rem;}
    .prep-login-sub{text-align:center;color:#64748b;font-size:.93rem;margin-bottom:1.6rem;}
    [data-testid="stSidebar"]{background:#0A355E;border-right:3px solid #B28A39;}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] label{color:#f1f5f9!important;}
    [data-testid="stSidebar"] [role="radiogroup"] label{border-radius:10px;padding:.25rem .4rem;}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.10);}
    [data-testid="stSidebar"] button{border-radius:10px;}
    div.stButton>button[kind="primary"],div.stFormSubmitButton>button[kind="primary"]{background:#0A355E;border-color:#0A355E;border-radius:10px;font-weight:600;}
    div.stButton>button[kind="primary"]:hover,div.stFormSubmitButton>button[kind="primary"]:hover{background:#124b7d;border-color:#124b7d;}
    div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:14px;}
    .prep-card{background:var(--secondary-background-color, #fff);border:1px solid rgba(100,116,139,.22);border-radius:14px;padding:17px 19px;min-height:118px;}
    .prep-kpi{font-size:1.85rem;font-weight:750;color:var(--text-color,#0A355E);line-height:1.3;overflow-wrap:anywhere;}
    .prep-muted{color:var(--text-color,#475569);opacity:.73;font-size:.9rem;}
    .prep-title{font-size:clamp(1.45rem,2.8vw,2rem);font-weight:800;color:var(--text-color,#14213D);margin-bottom:.25rem;line-height:1.2;}
    .prep-subtitle{color:var(--text-color,#475569);opacity:.7;margin-top:0;margin-bottom:1.3rem;}
    .prep-eyebrow{font-size:.77rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase;color:#B28A39;margin-bottom:.5rem;}
    .prep-note{border-left:3px solid #B28A39;padding:.65rem 1rem;background:rgba(178,138,57,.07);border-radius:0 10px 10px 0;margin:1rem 0;}
    @media(max-width:700px){.block-container{padding:1rem .85rem 2.5rem}.prep-card{min-height:100px;padding:13px}.prep-kpi{font-size:1.45rem}}
    </style>""",unsafe_allow_html=True)


def page_header(title, subtitle=None):
    st.markdown(f'<div class="prep-title">{escape(str(title))}</div>',unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="prep-subtitle">{escape(str(subtitle))}</div>',unsafe_allow_html=True)


def metric_card(title,value,foot=""):
    st.markdown(f'<div class="prep-card"><div class="prep-muted">{escape(str(title))}</div><div class="prep-kpi">{escape(str(value))}</div><div class="prep-muted">{escape(str(foot))}</div></div>',unsafe_allow_html=True)
