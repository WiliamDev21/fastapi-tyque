# Endpoint para quinielas
from fastapi import APIRouter, Form, Depends, status, HTTPException
from app.models.quiniela import Quiniela
from app.dependencies import get_db
from app.utils.utils import createCode

router = APIRouter(prefix="/api", tags=["Quinielas"])

# Endpoint para crear una nueva quiniela
@router.post("/quinielas/", response_model=Quiniela, status_code=status.HTTP_201_CREATED, summary="Crear una quiniela", description="Crea una nueva quiniela para una jornada.")
def create_quiniela(
    name: str = Form(..., description="Nombre de la quiniela"),
    jornadaCode: str = Form(..., description="Código de la jornada asociada"),
    db=Depends(get_db)
):
    """Crea una nueva quiniela para una jornada."""
    code = createCode(jornadaCode)
    
    # Crear la quiniela
    quiniela_data = {
        "code": code,
        "name": name,
        "jornadaCode": jornadaCode,
        "finalizada": False,
        "jugadores": []
    }
    db.quinielas.insert_one(quiniela_data)
    return Quiniela(**quiniela_data)

# Endpoint para obtener una quiniela por su código
@router.get("/quinielas/{quiniela_code}", response_model=Quiniela, status_code=status.HTTP_200_OK, summary="Obtener una quiniela", description="Obtiene la información de una quiniela por su código.")
def get_quiniela(quiniela_code: str, db=Depends(get_db)):
    """Obtiene la información de una quiniela por su código."""
    quiniela_data = db.quinielas.find_one({"code": quiniela_code})
    if not quiniela_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiniela no encontrada")
    return Quiniela(**quiniela_data)

# Endpoint para obtener todas las quinielas de una jornada
@router.get("/quinielas/jornada/{jornada_code}", response_model=list[Quiniela], status_code=status.HTTP_200_OK, summary="Obtener quinielas de una jornada", description="Obtiene todas las quinielas de una jornada específica.")
def get_quinielas_jornada(jornada_code: str, db=Depends(get_db)):
    """Obtiene todas las quinielas de una jornada específica."""
    quinielas_data = db.quinielas.find({"jornadaCode": jornada_code}, {"_id": 0, "jugadores": 0})
    if not quinielas_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron quinielas para esta jornada")
    return [Quiniela(**quiniela) for quiniela in quinielas_data]

# Endpoint para obetener quinielas que aun no terminaron
@router.get("/quinielas/actuales", response_model=list[Quiniela], status_code=status.HTTP_200_OK, summary="Obtener quinielas actuales", description="Obtiene la lista de quinielas que aún no han sido finalizadas.")
def get_quinielas_actuales(db=Depends(get_db)):
    """Obtiene la lista de quinielas que aún no han sido finalizadas."""
    quinielas_data = db.quinielas.find({"finalizada": False}, {"_id": 0, "jugadores": 0})
    if not quinielas_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron quinielas actuales")
    return [Quiniela(**quiniela) for quiniela in quinielas_data]