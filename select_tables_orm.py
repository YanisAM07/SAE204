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

Session = sessionmaker(bind=engine)
session = Session()

# - Lire tous les départements -
print("=== Départements ===")
departements = session.query(Departement).all()
for dep in departements:
    print(dep)

# - Lire toutes les formations avec leur département (via la relation) -
print("\n=== Formations ===")
formations = session.query(Formation).all()
for f in formations:
    print(f) # Affiche via la méthode __repr__ définie dans model.py

session.close()