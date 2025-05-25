# Configuración de Firebase Admin SDK para Google Cloud Storage
import firebase_admin
from firebase_admin import credentials, storage
import os
import json

# Configurar las credenciales de Firebase
if os.environ.get("FIREBASE_KEY_JSON"):
    print("FIREBASE_KEY_JSON encontrada")
    cred_dict = json.loads(os.environ["FIREBASE_KEY_JSON"])
    # Corregir saltos de línea en la clave privada si vienen escapados
    if "private_key" in cred_dict:
        # Asegura que todos los saltos de línea sean reales
        cred_dict["private_key"] = cred_dict["private_key"].replace('\\n', '\n').replace('\\\n', '\n')
        if '\\n' in cred_dict["private_key"] or '\\\n' in cred_dict["private_key"]:
            cred_dict["private_key"] = cred_dict["private_key"].replace('\\n', '\n').replace('\\\n', '\n')
    print(f"Credenciales: {cred_dict}")
    # Usar el diccionario de credenciales directamente en lugar de un archivo temporal
    cred = credentials.Certificate(cred_dict)
else:
    print("FIREBASE_KEY_JSON NO encontrada, buscando archivo...")
    FIREBASE_KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'serviceAccountKey.json')
    if not os.path.isfile(FIREBASE_KEY_PATH):
        FIREBASE_KEY_PATH = '/app/serviceAccountKey.json'
    cred = credentials.Certificate(FIREBASE_KEY_PATH)

# Obtener el bucket de variable de entorno o usar el valor por defecto
BUCKET_NAME = os.environ.get("FIREBASE_STORAGE_BUCKET", "tyque-bbad4.appspot.com")

firebase_admin.initialize_app(cred, {"storageBucket": BUCKET_NAME})

def upload_image_to_gcs(image, filename):
    """
    Sube una imagen (buffer BytesIO o UploadFile) a Google Cloud Storage.
    Si el objeto es un buffer BytesIO, se asume que es PNG y se usa content_type="image/png".
    """
    bucket = storage.bucket()
    blob = bucket.blob(filename)  # filename ya debe incluir la carpeta (ej: 'ligas/xxx.png')
    # Si es un buffer BytesIO, no tiene atributo content_type
    if hasattr(image, 'content_type'):
        content_type = image.content_type
    else:
        content_type = "image/png"
    blob.upload_from_file(image, content_type=content_type)
    blob.make_public()
    return blob.public_url
