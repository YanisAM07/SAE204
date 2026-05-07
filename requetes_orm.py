from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from model import Departement, Formation
from sqlalchemy import func # Nécessaire pour la fonction COUNT

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()

# 1. Filtrer : formations dont le nom commence par 'BUT'
print("=== Formations BUT ===")
buts = session.query(Formation).filter(Formation.nom.like("BUT%")).all()
for f in buts:
    print(f)

# 2. Filtrer : formations d'un département précis (via la relation)
print("\n=== Formations du département Informatique ===")
dep_info = session.query(Departement).filter(Departement.nom.like("%Informatique%")).first()
if dep_info:
    # Grâce à l'ORM, on peut juste parcourir la liste des formations liées à ce département !
    for f in dep_info.formations:
        print(f)

# 3. Compter : nombre de formations par département (GROUP BY)
print("\n=== Nombre de formations par département ===")
resultats = session.query(Departement.nom, func.count(Formation.id)) \
    .join(Formation) \
    .group_by(Departement.nom).all()

for nom, nb in resultats:
    print(f"{nom}: {nb} formation(s)")

session.close()