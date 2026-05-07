from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(url)

with engine.connect() as connection:
    connection.execute(text("""
        INSERT INTO departement (code, nom) VALUES
        ('INFO', 'Informatique'),
        ('MMI', 'Métiers du Multimédia et de l\\'Internet'),
        ('GEA', 'Gestion des Entreprises et des Administrations')
    """))
    connection.commit()
    print("Données insérées")