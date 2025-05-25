from pydantic import BaseModel, Field
from typing import Optional

class Partido(BaseModel):
    """Modelo que representa un partido de fútbol."""
    id: Optional[str] = Field(alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único del partido")
    fecha: str = Field(..., description="Fecha y hora del partido")
    equipoLocalCode: str = Field(..., description="Código del equipo local")
    equipoVisitanteCode: str = Field(..., description="Código del equipo visitante")
    finalizado: Optional[bool] = Field(default=False, description="Indica si el partido está finalizado")
    ganador: Optional[str] = Field(default=None, description="Código del equipo ganador")

