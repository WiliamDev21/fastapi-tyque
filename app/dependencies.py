# Archivo para dependencias reutilizables de FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

def get_db():
    # Prioridad: variable de entorno > .env > valor por defecto
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    mongo_uri = mongo_uri.replace("MONGO_URI=", "")  # Por si viene con prefijo
    print("MONGO_URI:", mongo_uri)
    client = MongoClient(mongo_uri)
    db = client["tyquedb"]
    try:
        yield db
    finally:
        client.close()

