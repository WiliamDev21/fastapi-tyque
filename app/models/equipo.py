from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.models.pyobjectid import PyObjectId


class Equipo(BaseModel):
    """Modelo que representa un equipo de fútbol."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único del equipo")
    name: str = Field(..., description="Nombre del equipo")
    img: str = Field(..., description="URL de la imagen del equipo")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}