from fastapi import APIRouter, UploadFile, File, Form, Depends, status, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.utils.gcs import upload_image_to_gcs, delete_image_from_gcs
from app.dependencies import get_db
from app.models.equipo import Equipo
from app.utils.utils import createCode, compressImage, validateKey

router = APIRouter(prefix="/api", tags=["Equipos"])

api_key_header = APIKeyHeader(name="API-KEY", auto_error=False)

def require_valid_key(api_key: str = Security(api_key_header)):
    if not api_key or not validateKey(api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida o no proporcionada")

# Endpoint para crear un nuevo equipo
@router.post("/equipos", response_model=Equipo, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo equipo", description="Crea un nuevo equipo y lo agrega a la liga especificada.")
async def create_equipo(
    ligaCode: str = Form(..., description="Código de la liga a la que pertenece el equipo"),
    name: str = Form(..., description="Nombre del equipo"),
    img: UploadFile = File(..., description="Imagen del equipo"),
    db = Depends(get_db),
    _: None = Depends(require_valid_key)
):
    """Crea un nuevo equipo y lo agrega a la liga correspondiente."""
    code = createCode(ligaCode)
    img_path = f"equipos/{code}.png"  # Carpeta equipos
    imgCompress = compressImage(await img.read())
    img_url = upload_image_to_gcs(imgCompress, img_path)
    equipo_data = {"code": code, "name": name, "img": img_url}
    db.ligas.update_one(
        {"code": ligaCode},
        {"$push": {"equipos": equipo_data}}
    )
    return Equipo(**equipo_data)

#Endpoint para obtener un equipo
@router.get("/equipos/{equipo_code}", response_model=Equipo, status_code=status.HTTP_200_OK, summary="Obtener un equipo", description="Obtiene la información de un equipo por su código.")
def get_equipo(equipo_code: str, db = Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene la información de un equipo por su código."""
    codeLiga = equipo_code[:5]
    equipo_data = db.ligas.find_one(
        {"code": codeLiga, "equipos.code": equipo_code},
        {"equipos.$": 1}
    )   
    if not equipo_data or "equipos" not in equipo_data or not equipo_data["equipos"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return Equipo(**equipo_data["equipos"][0])

# Endpoint para eliminar un equipo
@router.delete("/equipos/{equipo_code}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un equipo", description="Elimina un equipo por su código.")
def delete_equipo(equipo_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    codeLiga = equipo_code[:5]
    result = db.ligas.update_one(
        {"code": codeLiga},
        {"$pull": {"equipos": {"code": equipo_code}}}
    )
    delete_image_from_gcs(f"equipos/{equipo_code}.png")  # Eliminar imagen del equipo de GCS
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return
