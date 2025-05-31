# Configuración de Firebase Admin SDK para Google Cloud Storage
from google.cloud import storage
from dotenv import load_dotenv
import os
import json

def get_gcs_bucket():
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    if not BUCKET_NAME:
        load_dotenv()
        BUCKET_NAME = os.environ.get("BUCKET_NAME")
    client = storage.Client("serviceAccountKey.json")
    return client.bucket(BUCKET_NAME)


def upload_image_to_gcs(image, filename):
    """
    Sube una imagen (buffer BytesIO o UploadFile) a Google Cloud Storage.
    Si el objeto es un buffer BytesIO, se asume que es PNG y se usa content_type="image/png".
    """
    try:
        bucket = get_gcs_bucket()
        blob = bucket.blob(filename)
        if hasattr(image, 'content_type'):
            content_type = image.content_type
        else:
            content_type = "image/png"
        blob.upload_from_file(image, content_type=content_type)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print(f">>> gcs.py: ERROR en upload_image_to_gcs: {e}")
        raise


def delete_image_from_gcs(filename):
    """
    Elimina una imagen de Google Cloud Storage.
    """
    try:
        bucket = get_gcs_bucket()
        blob = bucket.blob(filename)
        blob.delete()
        return True
    except Exception as e:
        print(f">>> gcs.py: ERROR en delete_image_from_gcs: {e}")
        raise