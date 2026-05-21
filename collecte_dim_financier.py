from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, requests
from models_dimensions import TypeHonoraire, TypePrescription

load_dotenv()
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(url)
session = sessionmaker(bind=engine)()

BASE = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

print("=== Collecte types d'honoraires et prescriptions ===")

# Types d'honoraires
SELECT_H = "type_honoraire_niveau_1,type_honoraire_niveau_2,type_honoraire_niveau_3"
resp = requests.get(
    f"{BASE}/honoraires/records",
    params={"select": SELECT_H, "group_by": SELECT_H, "limit": 100}
)
for rec in resp.json().get("results", []):
    n1 = rec.get("type_honoraire_niveau_1") or None
    n2 = rec.get("type_honoraire_niveau_2") or None
    n3 = rec.get("type_honoraire_niveau_3") or None
    
    if n1:
        existe = session.query(TypeHonoraire).filter_by(niveau_1=n1, niveau_2=n2, niveau_3=n3).first()
        if not existe:
            session.add(TypeHonoraire(niveau_1=n1, niveau_2=n2, niveau_3=n3))
session.commit()
print(f" Types d'honoraires : {session.query(TypeHonoraire).count()}")

# Types de prescriptions
resp = requests.get(
    f"{BASE}/prescriptions/records",
    params={"select": "libelle_poste_prescription", "group_by": "libelle_poste_prescription", "limit": 100}
)
for rec in resp.json().get("results", []):
    libelle = rec.get("libelle_poste_prescription")
    if libelle and not session.query(TypePrescription).filter_by(libelle=libelle).first():
        session.add(TypePrescription(libelle=libelle))
session.commit()
print(f" Types de prescriptions : {session.query(TypePrescription).count()}")

session.close()
print("Terminé")