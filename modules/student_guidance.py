"""Diagnóstico estudiantil basado exclusivamente en evaluaciones oficiales publicadas."""
from collections import defaultdict
import pandas as pd
import streamlit as st
from modules import grading_admin
from modules.data import get_attempt_answers_v16


def _collect(attempts):
    courses = defaultdict(list)
    criteria = defaultdict(list)
    recommendations = []
    inspected = 0
    warnings = []
    for attempt in attempts:
        if attempt.get('grading_mode') != 'administrativa':
            continue
        aid = attempt.get('id')
        if not aid:
            continue
        try:
            official = grading_admin.published_result(aid)
            if not isinstance(official, dict) or not official.get('published'):
                continue
            details = grading_admin.published_rubric_details(aid) or []
            feedback = grading_admin.published_feedback(aid) or []
            answers = get_attempt_answers_v16(aid)
            names = {a['id']: a.get('course_name') or a.get('course_code') or 'Sin curso' for a in answers}
            for d in details:
                course = names.get(d.get('answer_id'), 'Sin curso')
                if d.get('answer_score') is not None:
                    courses[course].append(float(d['answer_score']))
                for item in d.get('criteria') or []:
                    mx = float(item.get('max_points') or 0)
                    if mx > 0:
                        criteria[str(item.get('criterion_name') or 'Sin criterio')].append(
                            100 * float(item.get('awarded_points') or 0) / mx)
            for f in feedback:
                suggestion = str(f.get('recommendation') or '').strip()
                if suggestion:
                    recommendations.append((names.get(f.get('answer_id'), 'Sin curso'), suggestion))
            inspected += 1
        except Exception as exc:
            warnings.append(f'No se pudo consultar un simulacro publicado: {type(exc).__name__}')
    return courses, criteria, recommendations, inspected, warnings


def render(attempts):
    st.markdown('### Diagnóstico y plan de estudio')
    st.caption('Solo se utilizan rúbricas y observaciones de evaluaciones administrativas oficialmente publicadas. Las notas pendientes nunca se incluyen.')
    eligible = [a for a in attempts if a.get('grading_mode') == 'administrativa' and a.get('status') == 'finalizado']
    if not eligible:
        st.info('Realiza un simulacro administrativo y espera su publicación para obtener tu diagnóstico.')
        return
    if not st.button('Actualizar mi diagnóstico', key='student_guidance_refresh'):
        st.caption('Selecciona «Actualizar mi diagnóstico» para consultar tus resultados oficiales más recientes.')
        return
    with st.spinner('Consultando evaluaciones publicadas...'):
        courses, criteria, recommendations, inspected, warnings = _collect(eligible[:30])
    if warnings:
        st.warning('Algunos datos no estuvieron disponibles. Intenta actualizar nuevamente.')
    if not inspected:
        st.info('Todavía no tienes evaluaciones administrativas publicadas disponibles para este diagnóstico.')
        return
    st.metric('Simulacros publicados analizados', inspected)
    def summary(groups, name):
        rows = [{'Área': k, 'Promedio (%)': round(sum(v)/len(v), 1), 'Respuestas / criterios': len(v)}
                for k, v in groups.items() if v]
        rows.sort(key=lambda x: (x['Promedio (%)'], x['Área']))
        if rows:
            st.markdown(f'**{name}**')
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        return rows
    course_rows = summary(courses, 'Desempeño por curso')
    criterion_rows = summary(criteria, 'Desempeño por criterio de rúbrica')
    st.markdown('#### Plan de estudio sugerido')
    weak_courses = [r for r in course_rows if r['Promedio (%)'] < 70]
    weak_criteria = [r for r in criterion_rows if r['Promedio (%)'] < 70]
    if weak_courses:
        st.write('**Prioridad de repaso por curso:** ' + ', '.join(r['Área'] for r in weak_courses[:5]))
    if weak_criteria:
        st.write('**Aspectos técnicos por fortalecer:** ' + ', '.join(r['Área'] for r in weak_criteria[:5]))
    if recommendations:
        st.write('**Recomendaciones escritas por el evaluador:**')
        seen = set()
        for course, note in recommendations:
            if (course, note) not in seen:
                st.markdown(f'- **{course}:** {note}')
                seen.add((course, note))
            if len(seen) >= 12:
                break
    if not weak_courses and not weak_criteria and not recommendations:
        st.success('No se identificaron áreas por debajo de 70% en los resultados disponibles. Continúa practicando y revisando tus respuestas.')
    st.caption('El umbral de 70% es orientativo para priorizar el estudio; no representa una nota mínima oficial de aprobación. El diagnóstico no modifica calificaciones.')
