
from datetime import date

CAREERS = {
    "IME": "Ingeniería Mecánica Eléctrica",
    "IE": "Ingeniería Eléctrica",
    "IEL": "Ingeniería Electrónica",
}

DEMO_USERS = {
    "estudiante@demo.gt": {
        "password": "demo123",
        "name": "Juan Pérez",
        "role": "estudiante",
        "career_code": "IE",
        "cohort": "EGP-2026-II",
        "student_id": "202012345",
    },
    "docente@demo.gt": {
        "password": "demo123",
        "name": "Ing. María López",
        "role": "docente",
        "career_code": "IE",
        "cohort": "EGP-2026-II",
    },
    "coordinacion@demo.gt": {
        "password": "demo123",
        "name": "Coordinación EIME",
        "role": "coordinador",
        "career_code": None,
        "cohort": "EGP-2026-II",
    },
    "admin@demo.gt": {
        "password": "demo123",
        "name": "Administrador PREP-EIME",
        "role": "administrador",
        "career_code": None,
        "cohort": "EGP-2026-II",
    },
}

AREAS = [
    ("Circuitos eléctricos", ["IE", "IEL", "IME"]),
    ("Electromagnetismo", ["IE", "IEL", "IME"]),
    ("Electrónica", ["IE", "IEL", "IME"]),
    ("Instrumentación", ["IE", "IEL", "IME"]),
    ("Conversión de energía", ["IE", "IEL", "IME"]),
    ("Máquinas eléctricas", ["IE", "IEL", "IME"]),
    ("Sistemas de control", ["IE", "IEL", "IME"]),
    ("Automatización", ["IE", "IEL", "IME"]),
    ("Sistemas eléctricos de potencia", ["IE", "IME"]),
    ("Instalaciones eléctricas", ["IE", "IME"]),
    ("Comunicaciones y telecomunicaciones", ["IEL", "IE"]),
    ("Ingeniería mecánica", ["IME"]),
    ("Energía térmica", ["IME"]),
    ("Diseño y mantenimiento", ["IME"]),
]

# Cursos demostrativos verificados visualmente en los pensum compartidos.
# Se incluyen como estructura inicial, no como contenido académico oficial.
COURSES = [
    {"code":"0206","name":"Circuitos Eléctricos 2","semester":6,"careers":["IE","IEL","IME"],"area":"Circuitos eléctricos"},
    {"code":"0210","name":"Teoría Electromagnética 1","semester":6,"careers":["IE","IEL","IME"],"area":"Electromagnetismo"},
    {"code":"0230","name":"Instrumentación Eléctrica","semester":7,"careers":["IE","IEL","IME"],"area":"Instrumentación"},
    {"code":"0232","name":"Electrónica 1","semester":7,"careers":["IE","IEL","IME"],"area":"Electrónica"},
    {"code":"0212","name":"Conversión de Energía Electromecánica 1","semester":7,"careers":["IE","IEL","IME"],"area":"Conversión de energía"},
    {"code":"0214","name":"Máquinas Eléctricas","semester":8,"careers":["IE","IEL","IME"],"area":"Máquinas eléctricas"},
    {"code":"0236","name":"Sistemas de Control 1","semester":8,"careers":["IE","IEL","IME"],"area":"Sistemas de control"},
    {"code":"0237","name":"Sistemas de Control 2","semester":9,"careers":["IE","IEL","IME"],"area":"Sistemas de control"},
    {"code":"0238","name":"Automatización Industrial","semester":10,"careers":["IE","IEL","IME"],"area":"Automatización"},
    {"code":"0218","name":"Líneas de Transmisión","semester":7,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0219","name":"Transmisión y Distribución","semester":8,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0220","name":"Análisis de Sistemas de Potencia 1","semester":9,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0224","name":"Alta Tensión","semester":9,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0221","name":"Sistemas de Generación","semester":10,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0222","name":"Protección de Sistemas de Potencia","semester":10,"careers":["IE","IME"],"area":"Sistemas eléctricos de potencia"},
    {"code":"0208","name":"Instalaciones Eléctricas","semester":10,"careers":["IE","IME"],"area":"Instalaciones eléctricas"},
    {"code":"0242","name":"Comunicaciones 1","semester":7,"careers":["IEL","IE"],"area":"Comunicaciones y telecomunicaciones"},
    {"code":"0244","name":"Comunicaciones 2","semester":8,"careers":["IEL"],"area":"Comunicaciones y telecomunicaciones"},
    {"code":"0245","name":"Comunicaciones 3","semester":9,"careers":["IEL"],"area":"Comunicaciones y telecomunicaciones"},
    {"code":"0243","name":"Comunicaciones 4","semester":10,"careers":["IEL"],"area":"Comunicaciones y telecomunicaciones"},
]

DEMO_QUESTIONS = [
    {
        "id": 1,
        "area": "Circuitos eléctricos",
        "course_code": "0206",
        "question": "Explique qué representa físicamente el factor de potencia y qué efectos produce un valor bajo en una instalación.",
        "difficulty": 3,
        "competency": "Analizar",
        "careers": ["IE","IEL","IME"],
    },
    {
        "id": 2,
        "area": "Máquinas eléctricas",
        "course_code": "0214",
        "question": "Explique el principio de funcionamiento de un transformador y cómo se relacionan tensión, corriente y número de espiras.",
        "difficulty": 3,
        "competency": "Explicar",
        "careers": ["IE","IEL","IME"],
    },
    {
        "id": 3,
        "area": "Sistemas eléctricos de potencia",
        "course_code": "0220",
        "question": "Ante una caída de tensión significativa al final de un alimentador, indique qué variables analizaría antes de proponer una solución.",
        "difficulty": 4,
        "competency": "Defender técnicamente",
        "careers": ["IE","IME"],
    },
]

def get_courses_for_career(career_code):
    return [c for c in COURSES if career_code in c["careers"]]

def get_areas_for_career(career_code):
    return [name for name, careers in AREAS if career_code in careers]

def get_questions_for_career(career_code):
    return [q for q in DEMO_QUESTIONS if career_code in q["careers"]]
