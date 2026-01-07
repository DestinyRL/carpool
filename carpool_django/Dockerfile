FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DOCKER_ENV=1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY . /app

ENV DJANGO_SETTINGS_MODULE=carpool_django.settings
ENV CARPOOL_SECRET_KEY=dev-secret-for-carpool-backend
ENV POSTGRES_DB=carpool
ENV POSTGRES_USER=carpool_user
ENV POSTGRES_PASSWORD=carpool_password
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

WORKDIR /app/carpool_django

# Run migrations at container start (entrypoint will run them too)
CMD ["sh", "-c", "python manage.py migrate --noinput && uvicorn carpool_django.asgi:application --host 0.0.0.0 --port 8000"]
