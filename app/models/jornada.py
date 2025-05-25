from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.partido import Partido

class Jornada(BaseModel):
    """Modelo que representa una jornada de una liga."""
    id: Optional[str] = Field(alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único de la jornada")
    ligaCode: str = Field(..., description="Código de la liga a la que pertenece la jornada")
    name: str = Field(..., description="Nombre de la jornada")
    fecha_inicio: str = Field(..., description="Fecha de inicio de la jornada")
    fecha_fin: str = Field(..., description="Fecha de fin de la jornada")
    partidos: List[Partido] = Field(..., description="Lista de partidos de la jornada")