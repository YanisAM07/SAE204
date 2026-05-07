from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Charger variables
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(url)

# Créer la table
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS departement (
            id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(20) NOT NULL UNIQUE,
            nom VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """))
    connection.commit()
    print("Table departement créée")