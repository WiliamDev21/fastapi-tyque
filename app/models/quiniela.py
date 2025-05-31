from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.pyobjectid import PyObjectId
from app.models.jugador import Jugador

class Quiniela(BaseModel):
    """Modelo que representa una quiniela de fútbol."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único de la quiniela")
    name: str = Field(..., description="Nombre de la quiniela")
    jornadaCode: str = Field(..., description="Código de la jornada asociada a la quiniela")
    finalizada: bool = Field(..., description="Indica si la quiniela está finalizada")
    jugadores: List[Jugador] = Field(..., description="Lista de jugadores que participan en la quiniela")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}