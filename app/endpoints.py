#Exportar todos los endpoints
from fastapi import APIRouter
from app.api.equiposEndpoint import router as equipos_router
from app.api.ligasEndpoint import router as ligas_router
from app.api.jornadaEndpoint import router as jornada_router
from app.api.partidosEndpoint import router as partidos_router
from app.api.quinielaEndpoint import router as quiniela_router

api_router = APIRouter()
api_router.include_router(equipos_router)
api_router.include_router(ligas_router)
api_router.include_router(jornada_router)
api_router.include_router(partidos_router)
api_router.include_router(quiniela_router)
