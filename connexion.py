from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Charger les variables depuis .env dans l'OS
load_dotenv()

# Récupérer les variables depuis l'OS
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

# Construction de la chaîne de connexion
url = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# Connexion à la base
engine = create_engine(url)

try:
    with engine.connect() as connection:
        print("Connexion réussie !")
except Exception as e:
    print("Échec de la connexion :", e)