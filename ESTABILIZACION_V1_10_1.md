# PREP-EIME v1.10.1 — estabilización de memoria

Cambios:
- Se elimina Plotly (paquete adicional) y se usa gráfico nativo de Streamlit.
- Se fija pyarrow<25 para evitar que Streamlit reinstale pyarrow 26 al iniciar.
- Bandeja administrativa: consulta acotada a los 80 simulacros más recientes (antes 200); la misma lista se reutiliza en el tablero, sin consultar de nuevo la tabla attempts.
- Diagnóstico estudiantil: máximo 10 intentos recientes por actualización manual (antes 30), sin modificar resultados almacenados.
- Se mantienen las evaluaciones, rúbricas, publicación, comentarios, Excel y seguridad existentes.

**Limitación:** la bandeja y analítica administrativas solo reflejan los 80 intentos más recientes; no es un informe histórico completo. El diagnóstico refleja hasta 10 intentos. No se borra ningún registro.

**Despliegue:** reemplazar los archivos de GitHub, incluido requirements.txt; reiniciar la app. No ejecutar SQL.

**Validación pendiente:** no hay acceso al entorno Supabase/Streamlit Cloud del usuario. Se verificó sintaxis y contenido ZIP, pero el consumo real de memoria debe comprobarse en el despliegue.
