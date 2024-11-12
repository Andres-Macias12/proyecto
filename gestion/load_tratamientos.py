import os
import django

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dentalcare.settings")
django.setup()

from gestion.models import Tratamiento 

# Lista de tratamientos que deseas cargar
tratamientos_data = [
    {'codigo': 'T001', 'tipo': 'Limpieza Dental'},
    {'codigo': 'T002', 'tipo': 'Relleno Dental'},
    {'codigo': 'T003', 'tipo': 'Extracción Dental'},
    {'codigo': 'T004', 'tipo': 'Tratamiento de Conducto'},
    {'codigo': 'T005', 'tipo': 'Implante Dental'},
    {'codigo': 'T006', 'tipo': 'Coronas Dentales'},
    {'codigo': 'T007', 'tipo': 'Puentes Dentales'},
    {'codigo': 'T008', 'tipo': 'Ortodoncia'},
    {'codigo': 'T009', 'tipo': 'Blanqueamiento Dental'},
    {'codigo': 'T010', 'tipo': 'Tratamiento de Encías'},
    {'codigo': 'T011', 'tipo': 'Selladores Dentales'},
    {'codigo': 'T012', 'tipo': 'Prótesis Dentales'},
    {'codigo': 'T013', 'tipo': 'Terapia de Mantenimiento Periodontal'},
    {'codigo': 'T014', 'tipo': 'Tratamiento para el Bruxismo'},
    {'codigo': 'T015', 'tipo': 'Cirugía Oral'},
    {'codigo': 'T016', 'tipo': 'Radiografías Dentales'},
    {'codigo': 'T017', 'tipo': 'Fluoroterapia'},
    {'codigo': 'T018', 'tipo': 'Sedación Dental'},
    {'codigo': 'T019', 'tipo': 'Odontopediatría'},
    {'codigo': 'T020', 'tipo': 'Tratamiento de Dientes Sensibles'},
    {'codigo': 'T021', 'tipo': 'Facetas Dentales'},
    {'codigo': 'T022', 'tipo': 'Cirugía de Hueso'},
    {'codigo': 'T023', 'tipo': 'Colocación de Carillas'},
    {'codigo': 'T024', 'tipo': 'Microdentistería'},
    {'codigo': 'T025', 'tipo': 'Tratamiento de Quistes Dentales'},
    {'codigo': 'T026', 'tipo': 'Extracciones de Muelas del Juicio'},
    {'codigo': 'T027', 'tipo': 'Rehabilitación Oral Completa'},
    {'codigo': 'T028', 'tipo': 'Terapia de Raíz'},
    {'codigo': 'T029', 'tipo': 'Cirugía Ortognática'},
    {'codigo': 'T030', 'tipo': 'Tratamiento de Halitosis'},
    {'codigo': 'T031', 'tipo': 'Coronas de Porcelana'},
    {'codigo': 'T032', 'tipo': 'Tratamientos de Desensibilización'},
    {'codigo': 'T033', 'tipo': 'Tratamiento de Oclusión'},
    {'codigo': 'T034', 'tipo': 'Implantes de Mini-implantes'},
    {'codigo': 'T035', 'tipo': 'Terapia con Ozono'},
    {'codigo': 'T036', 'tipo': 'Restauraciones Estéticas'},
    {'codigo': 'T037', 'tipo': 'Gingivectomía'},
    {'codigo': 'T038', 'tipo': 'Cirugía de Aumento de Encía'},
    {'codigo': 'T039', 'tipo': 'Rehabilitación sobre Implantes'},
    {'codigo': 'T040', 'tipo': 'Estética Dental'},
    {'codigo': 'T041', 'tipo': 'Endodoncia Retirada'},
    {'codigo': 'T042', 'tipo': 'Reparación de Dientes Rotos'},
    {'codigo': 'T043', 'tipo': 'Tratamiento de Necrosis Pulpar'},
    {'codigo': 'T044', 'tipo': 'Pulpotomía'},
    {'codigo': 'T045', 'tipo': 'Tratamiento de Infecciones Dentales'},
    {'codigo': 'T046', 'tipo': 'Asesoramiento sobre Higiene Oral'},
    {'codigo': 'T047', 'tipo': 'Sistemas de Ortodoncia Lingual'},
    {'codigo': 'T048', 'tipo': 'Tratamiento de Dientes Supernumerarios'},
    {'codigo': 'T049', 'tipo': 'Brackets Estéticos'},
    {'codigo': 'T050', 'tipo': 'Ortodoncia Invisible'},
    {'codigo': 'T051', 'tipo': 'Cirugía de Implantes Zigomáticos'},
    {'codigo': 'T052', 'tipo': 'Tratamiento de Tumores en la Boca'},
    {'codigo': 'T053', 'tipo': 'Odontología Estética'},
    {'codigo': 'T054', 'tipo': 'Bótox Dental'},
    {'codigo': 'T055', 'tipo': 'Tratamiento de Dientes Impactados'},
    {'codigo': 'T056', 'tipo': 'Recuperación de Dientes Perdidos'},
    {'codigo': 'T057', 'tipo': 'Técnicas de Relajación para Pacientes Dentales'},
    {'codigo': 'T058', 'tipo': 'Consultas para Dentaduras Completas'},
    {'codigo': 'T059', 'tipo': 'Biopsias de Tejidos Bucales'},
    {'codigo': 'T060', 'tipo': 'Alineadores Dentales Personalizados'},
    {'codigo': 'T061', 'tipo': 'Coronas de Zirconio'},
    {'codigo': 'T062', 'tipo': 'Tratamiento de Disfunción Temporomandibular (DTM)'},
    {'codigo': 'T063', 'tipo': 'Estudios Radiográficos Avanzados'},
    {'codigo': 'T064', 'tipo': 'Análisis de Siluetas y Contornos Dentales'},
    {'codigo': 'T065', 'tipo': 'Tratamientos Preventivos para Pacientes de Alto Riesgo'},
]

# Cargar cada tratamiento en la base de datos
for tratamiento_data in tratamientos_data:
    tratamiento, created = Tratamiento.objects.get_or_create(
        codigo=tratamiento_data["codigo"],
        defaults={
            "tipo": tratamiento_data["tipo"],
        }
    )
    if created:
        print(f"Tratamiento '{tratamiento.tipo}' con código '{tratamiento.codigo}' agregado a la base de datos.")
    else:
        print(f"Tratamiento '{tratamiento.tipo}' con código '{tratamiento.codigo}' ya existe en la base de datos.")  
