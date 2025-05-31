from PIL import Image
from io import BytesIO
import random
import string
import json

from fastapi import Depends
from ..dependencies import get_db

def createCode(firstCode="") -> str:
    # Genera un código alfanumérico de 5 caracteres
    random_code = ''.join(random.choices(
        string.ascii_letters + string.digits, k=5))
    return firstCode + random_code

def compressImage(archivo):
    """
    Comprime una imagen PNG recibida como UploadFile y retorna un buffer BytesIO listo para subir.
    compress_level: 0 (sin compresión) a 9 (máxima compresión, default 6)
    """
    image = Image.open(BytesIO(archivo))
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer

def actualizarAciertos(partido_code: str,ganador_code: str, db=Depends(get_db)):
    # Actualiza los aciertos de los jugadores en la quiniela
    jornada_code = partido_code[:5]
    quinielas = db.quinielas.find({"jornadaCode": jornada_code}, {"jugadores": 1})
    for quiniela in quinielas:
        for jugador in quiniela["jugadores"]:
            if jugador["predicciones"][partido_code] == ganador_code:
                db.quinielas.update_one(
                    {"code": quiniela["code"], "jugadores.code": jugador["code"]},
                    {"$inc": {"jugadores.$.aciertos": 1}}
                )

def validateKey(key: str):
    try: 
        with open("serviceAccountKey.json", "r") as file:
            data = json.load(file)
            file.close()
        return data.get("private_key") == key
    except Exception as e:
        print(f"Error al leer el archivo serviceAccountKey.json: {e}")
        return False