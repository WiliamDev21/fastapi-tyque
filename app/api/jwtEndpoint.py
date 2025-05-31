from fastapi import APIRouter, status
import json

router = APIRouter(prefix="/api", tags=["JWT"])

@router.post("/jwt",status_code=status.HTTP_200_OK)
async def jwt_endpoint(credential: dict):
    try:
        with open("serviceAccountKey.json", "w") as file:
            json.dump(credential, file)
        file.close()
        return {"message": "Credenciales guardadas correctamente en serviceAccountKey.json"}
    except Exception as e:
        print(f"Error al leer el archivo serviceAccountKey.json: {e}")
        return {"error": "No se pudo leer el archivo serviceAccountKey.json"}