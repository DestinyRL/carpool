FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DOCKER_ENV=1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY . /app
COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

ENV CARPOOL_SECRET_KEY=dev-secret-for-carpool-backend
ENV POSTGRES_DB=carpool
ENV POSTGRES_USER=carpool_user
ENV POSTGRES_PASSWORD=carpool_password
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

CMD ["/bin/bash", "-c", "/app/wait-for-postgres.sh db 5432 && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8080"]
