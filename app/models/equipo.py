from pydantic import BaseModel, Field
from typing import Optional

class Equipo(BaseModel):
    """Modelo que representa un equipo de fútbol."""
    id: Optional[str] = Field(alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único del equipo")
    name: str = Field(..., description="Nombre del equipo")
    img: str = Field(..., description="URL de la imagen del equipo")