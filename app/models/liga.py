#Modelo de liga
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.equipo import Equipo

class Liga(BaseModel):
    """Modelo que representa una liga de fútbol."""
    id: Optional[str] = Field(alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único de la liga")
    name: str = Field(..., description="Nombre de la liga")
    img: str = Field(..., description="URL de la imagen de la liga")
    equipos: List[Equipo] = Field(..., description="Lista de equipos que pertenecen a la liga")