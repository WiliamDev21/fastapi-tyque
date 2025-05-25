#Endpoint de partidos
from fastapi import APIRouter, Form, Depends, status, HTTPException
from app.models.partido import Partido
from app.dependencies import get_db
from app.utils.utils import createCode, actualizarAciertos
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Partidos"])

# Endpoint para crear un nuevo partido
@router.post("/partidos/", response_model=Partido, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo partido", description="Crea un nuevo partido y lo agrega a la jornada especificada.")
def create_partido(
    jornadaCode: str = Form(..., description="Código de la jornada a la que pertenece el partido"),
    equipoLocalCode: str = Form(..., description="Código del equipo local"),
    equipoVisitanteCode: str = Form(..., description="Código del equipo visitante"),
    fecha: datetime = Form(..., description="Fecha y hora del partido"),
    db=Depends(get_db)
):
    """Crea un nuevo partido y lo agrega a la jornada correspondiente."""
    code = createCode(jornadaCode)
    partido_data = {
        "code": code,
        "equipoLocalCode": equipoLocalCode,
        "equipoVisitanteCode": equipoVisitanteCode,
        "fecha": fecha,
    }
    db.jornadas.update_one(
        {"code": jornadaCode},
        {"$push": {"partidos": partido_data}}
    )
    return Partido(**partido_data)

# Endpoint para obtener un partido por su código
@router.get("/partidos/{partido_code}", response_model=Partido, status_code=status.HTTP_200_OK, summary="Obtener un partido", description="Obtiene la información de un partido por su código.")
def get_partido(partido_code: str, db=Depends(get_db)):
    """Obtiene la información de un partido por su código."""
    partido_data = db.jornadas.find_one(
        {"partidos.code": partido_code},
        {"partidos.$": 1}
    )
    if not partido_data or not partido_data.get("partidos"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return Partido(**partido_data["partidos"][0])

# Endpoint para obtener todos los partidos de una jornada
@router.get("/partidos/jornada/{jornada_code}", response_model=list[Partido], status_code=status.HTTP_200_OK, summary="Obtener partidos de una jornada", description="Obtiene todos los partidos de una jornada específica.")
def get_partidos_jornada(jornada_code: str, db=Depends(get_db)):
    """Obtiene todos los partidos de una jornada específica."""
    jornada_data = db.jornadas.find_one({"code": jornada_code}, {"partidos": 1})
    if not jornada_data or not jornada_data.get("partidos"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron partidos para esta jornada")
    return [Partido(**partido) for partido in jornada_data["partidos"]]

# Endpoint para finalizar un partido
@router.put("/partidos/{partido_code}/finalizar/{ganador_code}", response_model=Partido, status_code=status.HTTP_200_OK, summary="Finalizar un partido", description="Marca un partido como finalizado.")
def finalizar_partido(partido_code: str, db=Depends(get_db)):
    """Marca un partido como finalizado."""
    code_jornada = partido_code[:5]
    ganador_code = partido_code[5:]
    jornada = db.jornadas.find_one(
        {"code": code_jornada, "partidos.code": partido_code},
        {"partidos.$": 1}
    )
    if not jornada or not jornada.get("partidos"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    db.jornadas.update_one(
        {"code": code_jornada, "partidos.code": partido_code},
        {"$set": {"partidos.$.finalizado": True, "partidos.$.ganador": ganador_code}}
    )
    actualizarAciertos(partido_code, ganador_code, db)
    return Partido(**jornada["partidos"][0])