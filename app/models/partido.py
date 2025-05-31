from pydantic import BaseModel, Field
from typing import Optional
from app.models.pyobjectid import PyObjectId

class Partido(BaseModel):
    """Modelo que representa un partido de fútbol."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único del partido")
    jornada_code: str = Field(..., description="Código de la jornada a la que pertenece el partido")
    equipo_local: str = Field(..., description="Código del equipo local")
    equipo_visitante: str = Field(..., description="Código del equipo visitante")
    ganador: Optional[str] = Field(default=None, description="Código del equipo ganador (opcional)")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

