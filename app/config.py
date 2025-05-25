# Archivo para la configuración de la app FastAPI y CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import api_router

def get_app() -> FastAPI:
    app = FastAPI(
        title="API Tyque",
        description="API para gestión de quinielas y partidos de fútbol",
        version="1.0.0",
    )

    origins = [
        "http://localhost:5173",  # Tu frontend
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Permitir solo los orígenes definidos
        allow_credentials=True,
        allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
        allow_headers=["*"],  # Permitir todos los encabezados
    )
    app.include_router(api_router)


    return app
