# Dockerfile para FastAPI backend listo para Google Cloud Run
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

ENV PYTHONPATH=/app

EXPOSE 8080

#CMD ["sh", "-c", "ls -lR /app && sleep 300"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
