from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from model import Base # importe Base qui connaît Departement et Formation

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(url)

# Crée toutes les tables définies dans model.py si elles n'existent pas encore
Base.metadata.create_all(engine)
print("Tables créées (ou déjà existantes).")