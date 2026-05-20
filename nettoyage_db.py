from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(url)

with engine.connect() as conn:
    # table enfant d'abord
    conn.execute(text("DROP TABLE IF EXISTS formation"))
    # puis table parent
    conn.execute(text("DROP TABLE IF EXISTS departement"))
    conn.commit()

print("Tables de test supprimées.")