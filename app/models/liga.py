#Modelo de liga
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.equipo import Equipo
from app.models.pyobjectid import PyObjectId
class Liga(BaseModel):
    """Modelo que representa una liga de fútbol."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único de la liga")
    name: str = Field(..., description="Nombre de la liga")
    img: str = Field(..., description="URL de la imagen de la liga")
    equipos: List[Equipo] = Field(default_factory=list, description="Lista de equipos de la liga")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}