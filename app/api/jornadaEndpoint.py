#Endpoint de jornadas
from fastapi import APIRouter, Form, Depends, status, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.models.jornada import Jornada
from app.dependencies import get_db
from app.utils.utils import createCode, validateKey
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Jornadas"])

api_key_header = APIKeyHeader(name="API-KEY", auto_error=False)

def require_valid_key(api_key: str = Security(api_key_header)):
    if not api_key or not validateKey(api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida o no proporcionada")

# Endpoint para crear una nueva jornada
@router.post("/jornadas", response_model=Jornada, status_code=status.HTTP_201_CREATED, summary="Crear una jornada", description="Crea una nueva jornada para una liga.")
def create_jornada(
    ligaCode: str = Form(..., description="Código de la liga a la que pertenece la jornada"),
    name: str = Form(..., description="Nombre de la jornada"),
    fecha_inicio: datetime = Form(..., description="Fecha de inicio de la jornada"),
    fecha_fin: datetime = Form(..., description="Fecha de fin de la jornada"),
    db=Depends(get_db),
    _: None = Depends(require_valid_key)
):
    """Crea una nueva jornada para una liga."""
    code = createCode()
    
    # Crear la jornada
    jornada_data = {
        "code": code,
        "ligaCode": ligaCode,
        "name": name,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "partidos": []
    }
    db.jornadas.insert_one(jornada_data)
    return Jornada(**jornada_data)

# Endpoint para obtener una jornada por su código
@router.get("/jornadas/{jornada_code}", response_model=Jornada, status_code=status.HTTP_200_OK, summary="Obtener una jornada", description="Obtiene la información de una jornada por su código.")
def get_jornada(jornada_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene la información de una jornada por su código."""
    jornada_data = db.jornadas.find_one({"code": jornada_code})
    if not jornada_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    return Jornada(**jornada_data)

# Endpoint para obtener las jornadas que aun no terminaron
@router.get("/jornadas/actuales", response_model=list[Jornada], status_code=status.HTTP_200_OK, summary="Obtener jornadas actuales", description="Obtiene la lista de jornadas que aún no han terminado.")
def get_jornadas_actuales(db=Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene la lista de jornadas que aún no han terminado."""
    fecha_actual = datetime.now()
    # Buscar jornadas actuales directamente en la colección 'jornadas'
    jornadas_data = db.jornadas.find({"fecha_fin": {"$gte": fecha_actual}})
    jornadas_no_terminadas = []
    for jornada in jornadas_data:
        jornada_sin_partidos = dict(jornada)
        jornada_sin_partidos.pop("partidos", None)
        jornadas_no_terminadas.append(Jornada(**jornada_sin_partidos))
    return jornadas_no_terminadas

# Endpoint para obtener todas las jornadas de una liga
@router.get("/jornadas/liga/{liga_code}", response_model=list[Jornada], status_code=status.HTTP_200_OK, summary="Obtener jornadas de una liga", description="Obtiene todas las jornadas de una liga específica.")
def get_jornadas_liga(liga_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    """Obtiene todas las jornadas de una liga específica."""
    # Buscar jornadas de la liga especificada
    jornadas_data = db.jornadas.find({"ligaCode": liga_code})
    if not jornadas_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron jornadas para esta liga")
    return [Jornada(**jornada) for jornada in jornadas_data]

# Endpoint para eliminar una jornada por su código
@router.delete("/jornadas/{jornada_code}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una jornada", description="Elimina una jornada por su código.")
def delete_jornada(jornada_code: str, db=Depends(get_db), _: None = Depends(require_valid_key)):
    result = db.jornadas.delete_one({"code": jornada_code})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    return