from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.jugador import Jugador

class Quiniela(BaseModel):
    """Modelo que representa una quiniela de fútbol."""
    id: Optional[str] = Field(alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único de la quiniela")
    name: str = Field(..., description="Nombre de la quiniela")
    jornadaCode: str = Field(..., description="Código de la jornada asociada a la quiniela")
    finalizada: bool = Field(..., description="Indica si la quiniela está finalizada")
    jugadores: List[Jugador] = Field(..., description="Lista de jugadores que participan en la quiniela")