from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from models_dimensions import Base

load_dotenv()
url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(url)
Base.metadata.create_all(engine)

print("Tables créées :")
for t in Base.metadata.tables: 
    print(f" - {t}")