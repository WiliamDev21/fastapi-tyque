# Endpoint para las ligas

from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile, Security
from app.models.liga import Liga
from app.dependencies import get_db
from typing import List
from app.utils.gcs import upload_image_to_gcs, delete_image_from_gcs
from app.utils.utils import createCode, compressImage, validateKey
from fastapi.security import APIKeyHeader

router = APIRouter(prefix="/api", tags=["Ligas"])

api_key_header = APIKeyHeader(name="API-KEY", auto_error=False)

def require_valid_key(api_key: str = Security(api_key_header)):
    if not api_key or not validateKey(api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida o no proporcionada")

# Endpoint para crear una liga
@router.post("/ligas", response_model=Liga, status_code=status.HTTP_201_CREATED, summary="Crear una liga", description="Crea una nueva liga de fútbol.")
async def create_liga(
        name: str = Form(..., description="Nombre de la liga"),
        img: UploadFile = File(..., description="Imagen de la liga"),
        db=Depends(get_db),
        _: None = Depends(require_valid_key)):
    """Crea una nueva liga de fútbol."""
    try:
        # Generar un código único para la liga
        code = createCode()
        print(f"Creando liga: {name} con código: {code}")
        img_path = f"ligas/{code}.png"
        print(f"Subiendo imagen a: {img_path}")
        # Comprimir la imagen antes de subirla
        img_content = await img.read()
        imgCompress = compressImage(img_content)
        print(f"Imagen comprimida: {imgCompress}")
        # Subir imagen a Google Cloud Storage
        
        img_url = upload_image_to_gcs(imgCompress, img_path)
        print(f"Imagen subida: {img_url}")
        liga_data = {
            "code": code,
            "name": name,
            "img": img_url,
            "equipos": []
        }
        print(f"Datos de la liga: {liga_data}")
        db.ligas.insert_one(liga_data)
        print(f"Liga creada: {liga_data}")
        return Liga(**liga_data)
    except Exception as e:
        print(f"Error creando liga: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la liga: {e}")


# Endpoint para obtener una lista con todas las ligas
@router.get("/ligas", response_model=List[Liga], status_code=status.HTTP_200_OK, summary="Obtener todas las ligas", description="Obtiene una lista de todas las ligas registradas.")
def get_ligas(db=Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene una lista de todas las ligas registradas sin la lista de equipos."""
    ligas = db.ligas.find()
    ligas_sin_equipos = []
    for liga in ligas:
        liga_dict = dict(liga)
        liga_dict.pop('equipos', None)  # Elimina la lista de equipos si existe
        ligas_sin_equipos.append(Liga(**liga_dict))
    return ligas_sin_equipos


# Endpoint para obtener una liga por su código
@router.get("/ligas/{liga_code}", response_model=Liga, status_code=status.HTTP_200_OK, summary="Obtener una liga", description="Obtiene la información de una liga por su código.")
def get_liga(liga_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene la información de una liga por su código."""
    liga_data = db.ligas.find_one({"code": liga_code})
    if not liga_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    return Liga(**liga_data)


# Endpoint para eliminar una liga por su código
@router.delete("/ligas/{liga_code}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una liga", description="Elimina una liga por su código.")
def delete_liga(liga_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    result = db.ligas.delete_one({"code": liga_code})
    delete_image_from_gcs(f"ligas/{liga_code}.png")  # Eliminar imagen de la liga de GCS
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    return


