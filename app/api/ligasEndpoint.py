# Endpoint para las ligas

from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from app.models.liga import Liga
from app.dependencies import get_db
from typing import List
from app.utils.gcs import upload_image_to_gcs
from app.utils.utils import createCode, compressImage

router = APIRouter(prefix="/api", tags=["Ligas"])

# Endpoint para crear una liga
@router.post("/ligas/", response_model=Liga, status_code=status.HTTP_201_CREATED, summary="Crear una liga", description="Crea una nueva liga de fútbol.")
async def create_liga(
        name: str = Form(..., description="Nombre de la liga"),
        img: UploadFile = File(..., description="Imagen de la liga"),
        db=Depends(get_db)):
    """Crea una nueva liga de fútbol."""
    # Generar un código único para la liga
    code = createCode()
    print(f"Creando liga: {name} con código: {code}")
    img_path = f"ligas/{code}.png"
    print(f"Subiendo imagen a: {img_path}")
    # Comprimir la imagen antes de subirla
    imgCompress = compressImage(await img.read())
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


# Endpoint para obtener una lista con todas las ligas
@router.get("/ligas/", response_model=List[Liga], status_code=status.HTTP_200_OK, summary="Obtener todas las ligas", description="Obtiene una lista de todas las ligas registradas.")
def get_ligas(db=Depends(get_db)):
    """Obtiene una lista de todas las ligas registradas."""
    ligas = db.ligas.find()
    return [Liga(**liga) for liga in ligas]


# Endpoint para obtener una liga por su código
@router.get("/ligas/{liga_code}", response_model=Liga, status_code=status.HTTP_200_OK, summary="Obtener una liga", description="Obtiene la información de una liga por su código.")
def get_liga(liga_code: str, db=Depends(get_db)):
    """Obtiene la información de una liga por su código."""
    liga_data = db.ligas.find_one({"code": liga_code})
    if not liga_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    return Liga(**liga_data)


