from pydantic import BaseModel, Field
from typing import Optional
from app.models.pyobjectid import PyObjectId

class Jugador(BaseModel):
    """
    Modelo que representa a un jugador de quiniela.
    - code: Código único del jugador.
    - name: Nombre del jugador.
    - respuestas: Diccionario con las respuestas del jugador (clave: partido, valor: respuesta).
    - aciertos: Número de aciertos del jugador.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID único en la base de datos")
    code: str = Field(..., description="Código único del jugador")
    name: str = Field(..., description="Nombre del jugador")
    respuestas: dict[str, str] = Field(..., description="Respuestas del jugador para cada partido")
    aciertos: int = Field(default=0, description="Cantidad de aciertos del jugador")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}