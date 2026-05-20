from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, requests
from models_dimensions import TypeExercice, TypeSecteur

load_dotenv()
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(url)
session = sessionmaker(bind=engine)()

BASE = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

print("=== Collecte types d'exercice et secteurs ===")

# --- Types d'exercice ---
resp = requests.get(
    f"{BASE}/demographie-exercices-liberaux/records",
    params={"select": "libelle_type_exercice_liberal", "group_by": "libelle_type_exercice_liberal", "limit": 50}
)
for rec in resp.json().get("results", []):
    libelle = rec.get("libelle_type_exercice_liberal")
    if libelle and not session.query(TypeExercice).filter_by(libelle=libelle).first():
        session.add(TypeExercice(libelle=libelle))
session.commit()
print(f" Types d'exercice : {session.query(TypeExercice).count()}")

# --- Secteurs conventionnels ---
SECTEURS = [
    ("S1", "Secteur 1 - Honoraires opposables"),
    ("S2", "Secteur 2 - Honoraires libres avec tact et mesure"),
    ("S2_OPTAM", "Secteur 2 avec OPTAM (Option Pratique Tarifaire Maîtrisée)"),
    ("NC", "Non conventionné")
]

for code, libelle in SECTEURS:
    if not session.query(TypeSecteur).filter_by(code=code).first():
        session.add(TypeSecteur(code=code, libelle=libelle))
session.commit()
print(f" Secteurs conventionnels : {session.query(TypeSecteur).count()}")

session.close()
print("=== Terminé ===")