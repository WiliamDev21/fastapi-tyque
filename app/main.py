from app.config import get_app
from fastapi import status

app = get_app()

@app.get("/api",status_code=status.HTTP_200_OK, summary="Check API", description="Check if the API is running")
def check():
    return {"message": "API is running"}
