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

ENV DJANGO_SETTINGS_MODULE=carpool_django.settings
ENV CARPOOL_SECRET_KEY=dev-secret-for-carpool-backend
ENV POSTGRES_DB=carpool
ENV POSTGRES_USER=carpool_user
ENV POSTGRES_PASSWORD=carpool_password
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

# Run migrations and start Django development server
CMD ["/bin/bash", "-c", "/app/wait-for-postgres.sh db 5432 && cd /app/carpool_django && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
