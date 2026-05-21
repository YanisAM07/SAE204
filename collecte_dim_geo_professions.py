from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, requests
from models_dimensions import Region, Departement, ProfessionSante, TrancheAge, Sexe

load_dotenv()
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(url)
session = sessionmaker(bind=engine)()

BASE = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"
DS = "demographie-effectifs-et-les-densites"

def get_distinct(select_fields, group_by_fields):
    """Retourne les valeurs distinctes via group_by (1 seule requête)."""
    params = {"select": select_fields, "group_by": group_by_fields, "limit": 100}
    return requests.get(f"{BASE}/{DS}/records", params=params).json().get("results", [])

def ajouter_si_absent(session, Model, **kwargs):
    """Insère l'objet uniquement s'il n'existe pas déjà."""
    filtre = {k: v for k, v in kwargs.items() if v is not None}
    if not session.query(Model).filter_by(**filtre).first():
        session.add(Model(**kwargs))

print(" Collecte dimensions géographiques et professions")

# Régions
for rec in get_distinct("region, libelle_region", "region, libelle_region"):
    ajouter_si_absent(session, Region, code=rec.get("region"), libelle=rec.get("libelle_region"))
session.commit()
print(f" Régions : {session.query(Region).count()}")

#Départements
region_map = {r.code: r.id for r in session.query(Region).all()}
for rec in get_distinct("departement, libelle_departement, region", "departement, libelle_departement, region"):
    code = rec.get("departement")
    libelle = rec.get("libelle_departement")
    rcode = rec.get("region")
    
    if code and libelle and rcode in region_map:
        ajouter_si_absent(session, Departement, code=code, libelle=libelle, region_id=region_map[rcode])
session.commit()
print(f" Départements : {session.query(Departement).count()}")

# Professions
for rec in get_distinct("profession_sante", "profession_sante"):
    if rec.get("profession_sante"):
        ajouter_si_absent(session, ProfessionSante, libelle=rec["profession_sante"])
session.commit()
print(f" Professions : {session.query(ProfessionSante).count()}")

#Tranches d'âge
for rec in get_distinct("libelle_classe_age", "libelle_classe_age"):
    if rec.get("libelle_classe_age"):
        ajouter_si_absent(session, TrancheAge, libelle=rec["libelle_classe_age"])
session.commit()
print(f" Tranches d'âge : {session.query(TrancheAge).count()}")

#  Sexe
for rec in get_distinct("libelle_sexe", "libelle_sexe"):
    if rec.get("libelle_sexe"):
        ajouter_si_absent(session, Sexe, libelle=rec["libelle_sexe"])
session.commit()
print(f" Sexe : {session.query(Sexe).count()}")

session.close()
print("Terminé")