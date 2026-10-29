"""Biblioteca mixta: consultas acotadas y permisos reforzados mediante RLS."""
import re
import uuid
import streamlit as st
from .supabase_client import get_supabase_client
from .data import get_courses_for_career, get_all_courses

BUCKET = "prep-library"
TYPES = {"guia":"Guía de estudio", "documento":"Documento PDF", "bibliografia":"Bibliografía", "enlace":"Enlace académico"}


def _client():
    return get_supabase_client(require_auth=True)


def _resources(client, course, admin=False, page=0):
    q = client.table('library_resource_courses').select('resource_id').eq('course_code',course).range(page*20,page*20+19)
    ids = [r['resource_id'] for r in (q.execute().data or [])]
    if not ids: return []
    q = client.table('library_resources').select('id,title,description,resource_type,author,publication_year,url,storage_path,unit_label,status,created_at').in_('id',ids)
    if not admin: q=q.eq('status','publicado')
    return q.order('created_at',desc=True).execute().data or []


def library_view(user):
    st.title('Biblioteca académica')
    st.caption('Guías, bibliografía, documentos y recursos de preparación para el EGP')
    client = _client()
    if not client:
        st.warning('La biblioteca requiere una sesión válida con Supabase.')
        return
    admin = user.get('role') == 'administrador'
    career = user.get('career_code')
    courses = get_all_courses() if admin else get_courses_for_career(career)
    if not courses:
        st.info('No hay cursos disponibles para esta carrera.')
        return
    course_map = {x['code']: x['name'] for x in courses}
    selected = st.selectbox('Curso',list(course_map),format_func=lambda c:f'{c} · {course_map[c]}',key='lib_course')
    page = st.number_input('Página',min_value=1,max_value=100,step=1,key='lib_page') - 1
    try:
        rows = _resources(client,selected,admin,page)
    except Exception:
        st.error('No se pudo consultar la biblioteca. Verifica que la migración 1.12.0 esté aplicada.')
        return
    if not rows: st.info('No hay recursos disponibles para este curso en esta página.')
    for r in rows:
        with st.container(border=True):
            st.subheader(r['title'])
            st.caption(f"{TYPES.get(r['resource_type'],r['resource_type'])} · {r.get('unit_label') or 'Todas las unidades'}" + (f" · {r['status']}" if admin else ''))
            if r.get('description'): st.write(r['description'])
            if r.get('author'): st.caption(f"Autor: {r['author']}" + (f" ({r['publication_year']})" if r.get('publication_year') else ''))
            if r.get('url'): st.link_button('Abrir recurso externo',r['url'])
            if r.get('storage_path'):
                if st.button('Generar acceso al PDF',key=f"lib_open_{r['id']}"):
                    try:
                        signed=client.storage.from_(BUCKET).create_signed_url(r['storage_path'],120)
                        url=signed.get('signedURL') or signed.get('signedUrl') or signed.get('signed_url')
                        if url:
                            st.session_state[f"lib_signed_{r['id']}"] = url
                            st.session_state[f"lib_signed_at_{r['id']}"] = __import__('time').time()
                        else: st.error('No se pudo generar el enlace.')
                    except Exception: st.error('No se pudo autorizar la descarga.')
                import time
                signed_key=f"lib_signed_{r['id']}"
                if st.session_state.get(signed_key) and time.time()-st.session_state.get(f"lib_signed_at_{r['id']}",0)<110:
                    st.link_button('Abrir PDF (enlace temporal)',st.session_state[signed_key])
    if admin:
        st.divider()
        st.subheader('Gestión de biblioteca')
        st.caption('Los recursos nuevos se crean en borrador y se publican tras revisión.')
        with st.form('lib_add',clear_on_submit=True):
            title=st.text_input('Título',max_chars=180)
            kind=st.selectbox('Tipo',list(TYPES),format_func=lambda k:TYPES[k])
            description=st.text_area('Descripción o contenido de la guía')
            author=st.text_input('Autor o institución')
            year=st.number_input('Año de publicación (0 = sin dato)',min_value=0,max_value=2100,value=0)
            unit=st.text_input('Unidad temática (opcional)')
            url=st.text_input('URL HTTPS (opcional)')
            pdf=st.file_uploader('PDF (opcional, máximo 10 MB)',type=['pdf'])
            all_courses=st.multiselect('Cursos asociados',list(course_map),default=[selected],format_func=lambda c:f'{c} · {course_map[c]}')
            submitted=st.form_submit_button('Guardar recurso en borrador')
        if submitted:
            if len(title.strip())<4 or not all_courses: st.error('Ingresa un título válido y al menos un curso.')
            elif url and not re.fullmatch(r'https://[^\s]+',url): st.error('El enlace debe utilizar HTTPS.')
            elif pdf and (pdf.size>10*1024*1024 or not pdf.getvalue().startswith(b'%PDF-')): st.error('PDF inválido o mayor de 10 MB.')
            elif kind in ('documento','enlace') and not (url or pdf): st.error('Este tipo requiere un enlace o un PDF.')
            else:
                rid=str(uuid.uuid4()); path=f'{rid}.pdf' if pdf else None
                try:
                    client.table('library_resources').insert({'id':rid,'title':title.strip(),'description':description,'resource_type':kind,'author':author,'publication_year':year or None,'url':url or None,'storage_path':path,'unit_label':unit,'status':'borrador'}).execute()
                    if pdf: client.storage.from_(BUCKET).upload(path,pdf.getvalue(),{'content-type':'application/pdf'})
                    client.table('library_resource_courses').insert([{'resource_id':rid,'course_code':c} for c in all_courses]).execute()
                    st.success('Recurso guardado en borrador. Puedes publicarlo desde la lista.')
                except Exception:
                    st.error('No se completó el registro. Revisa permisos, migración y configuración de Storage.')
        for r in rows:
            new_status=st.selectbox(f"Estado: {r['title']}",['borrador','publicado','archivado'],index=['borrador','publicado','archivado'].index(r['status']),key=f"lib_status_{r['id']}")
            if new_status != r['status'] and st.button(f"Aplicar estado: {r['title']}",key=f"lib_apply_{r['id']}"):
                try:
                    client.table('library_resources').update({'status':new_status}).eq('id',r['id']).execute()
                    st.success('Estado actualizado.'); st.rerun()
                except Exception: st.error('No se pudo actualizar el estado.')
