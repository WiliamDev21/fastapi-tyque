# Endpoint para los jugadores de las quinielas
from fastapi import APIRouter, Form, Depends, status, HTTPException
from app.models.jugador import Jugador
from app.dependencies import get_db
from app.utils.utils import createCode

router = APIRouter(prefix="/api", tags=["Jugadores"])

# Endpoint para crear un nuevo jugador
@router.post("/jugadores/", response_model=Jugador, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo jugador", description="Crea un nuevo jugador y lo agrega al equipo especificado.")
def create_jugador(
    quinielaCode: str = Form(..., description="Código de la quiniela a la que pertenece el jugador"),
    name: str = Form(..., description="Nombre del jugador"),
    db=Depends(get_db)
):
    """Crea un nuevo jugador y lo agrega a la quiniela correspondiente."""
    code = createCode(quinielaCode)
    jugador_data = {
        "code": code,
        "name": name,
        "quinielaCode": quinielaCode,
        "aciertos": 0,
        "predicciones": dict()
    }
    db.quinielas.update_one(
        {"code": quinielaCode},
        {"$push": {"jugadores": jugador_data}}
    )
    return Jugador(**jugador_data)

# Endpoint para obtener un jugador por su código
@router.get("/jugadores/{jugador_code}", response_model=Jugador, status_code=status.HTTP_200_OK, summary="Obtener un jugador", description="Obtiene la información de un jugador por su código.")
def get_jugador(jugador_code: str, db=Depends(get_db)):
    """Obtiene la información de un jugador por su código."""
    code_quiniela = jugador_code[:5]
    jugador_data = db.quinielas.find_one(
        {"code": code_quiniela, "jugadores.code": jugador_code},
        {"jugadores.$": 1}
    )
    if not jugador_data or "jugadores" not in jugador_data or not jugador_data["jugadores"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return Jugador(**jugador_data["jugadores"][0])

# Endpoint para obtener todos los jugadores de una quiniela
@router.get("/jugadores/quiniela/{quiniela_code}", response_model=list[Jugador], status_code=status.HTTP_200_OK, summary="Obtener jugadores de una quiniela", description="Obtiene todos los jugadores de una quiniela específica.")
def get_jugadores_quiniela(quiniela_code: str, db=Depends(get_db)):
    """Obtiene todos los jugadores de una quiniela específica."""
    quiniela_data = db.quinielas.find_one({"code": quiniela_code}, {"jugadores": 1})
    if not quiniela_data or not quiniela_data.get("jugadores"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron jugadores para esta quiniela")
    return [Jugador(**jugador) for jugador in quiniela_data["jugadores"]]

# Endpoint para agregar las predicciones de un jugador
@router.put("/jugadores/{jugador_code}/predicciones", response_model=Jugador, status_code=status.HTTP_200_OK, summary="Agregar predicciones de un jugador", description="Agrega las predicciones de un jugador para una quiniela.")
def agregar_predicciones_jugador(
    jugador_code: str,
    predicciones: dict = Form(..., description="Predicciones del jugador en formato JSON"),
    db=Depends(get_db)
):
    """Agrega las predicciones de un jugador para una quiniela."""
    code_quiniela = jugador_code[:5]
    result = db.quinielas.update_one(
        {"code": code_quiniela, "jugadores.code": jugador_code},
        {"$set": {"jugadores.$.predicciones": predicciones}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    
    jugador_data = db.quinielas.find_one(
        {"code": code_quiniela, "jugadores.code": jugador_code},
        {"jugadores.$": 1}
    )
    return Jugador(**jugador_data["jugadores"][0])

    