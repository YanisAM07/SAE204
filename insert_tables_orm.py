from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from model import Departement, Formation

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(url)

# Création de la session ORM
Session = sessionmaker(bind=engine)
session = Session()

# - Insérer les départements -
mmi = Departement(code="MMI_ORM", nom="Métiers du Multimédia et de l'Internet")
gea = Departement(code="GEA_ORM", nom="Gestion des Entreprises et des Administrations")
info = Departement(code="INFO_ORM", nom="Informatique")

session.add_all([info, mmi, gea])
session.commit() # les ids sont maintenant attribués automatiquement
print("Départements insérés.")

# - Insérer les formations en utilisant les objets Python directement -
session.add_all([
    Formation(nom="BUT Informatique", departement=info),
    Formation(nom="LP Cybersécurité", departement=info),
    Formation(nom="BUT MMI", departement=mmi),
    Formation(nom="BUT GEA", departement=gea)
])
session.commit()
print("Formations insérées.")

session.close()