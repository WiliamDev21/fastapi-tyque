import datetime
from app.config import get_app
from fastapi import status

app = get_app()

@app.get("/api",status_code=status.HTTP_200_OK, summary="Check API", description="Check if the API is running")
def check():
    print("API is running, datetime:", datetime.datetime.now())
    return {"message": "API is running"}
