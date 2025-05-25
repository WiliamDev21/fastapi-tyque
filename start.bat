REM Script para iniciar la aplicación FastAPI en modo producción


call venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
