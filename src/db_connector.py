from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json
import os

load_dotenv()
#postgresql://myuser:mypassword@localhost:5432/mydatabase Azure Key Vault
with open('credentials.json', 'r') as f:
    credentials = json.load(f)

user = credentials.get("user")  # Asegúrate de agregar el campo 'user' en tu JSON
password = credentials.get("password")
database = credentials.get("database")
host = credentials.get("host")

# Construye la URL de la base de datos
DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
