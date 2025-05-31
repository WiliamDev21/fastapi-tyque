# Dockerfile para FastAPI backend listo para Google Cloud Run
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y tzdata ntpdate && ln -fs /usr/share/zoneinfo/America/Mexico_City /etc/localtime && dpkg-reconfigure -f noninteractive tzdata && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY serviceAccountKey.json /app/serviceAccountKey.json

EXPOSE 8080


#CMD ["sh", "-c", "ls -lR /app && sleep 300"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
