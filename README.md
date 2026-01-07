# Carpool Backend (Django + FastAPI)

This repository provides a headless Python backend for a Carpool app.

Overview
- Django: core data management, admin UI, REST API (DRF) and JWT auth (SimpleJWT).
- FastAPI: high-performance ride search and WebSocket GPS tracking.
- Shared SQLite database file: `carpool_django/carpool.db`.

Requirements
- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
```

Running
- Start both servers (Django on 8000, FastAPI on 8080):

```bash
python run.py
```

This will run `manage.py migrate` for Django automatically before starting the dev server.

Configuration
- Shared SECRET_KEY: set environment variable `CARPOOL_SECRET_KEY` before running to use a production secret.
- CORS: both servers allow all origins by default (development). Tighten for production.

Django (carpool_django)
- Models: `User`, `Vehicle`, `Ride`, `Booking` (in `core.models`).
- Admin: all models are registered in Django Admin (`/admin/`).
- API endpoints (DRF router):
  - `/api/vehicles/`
  - `/api/rides/`
  - `/api/bookings/`
- JWT endpoints:
  - `/api/token/` (obtain)
  - `/api/token/refresh/`

FastAPI
- Ride search endpoint:
  - `GET /search?q=term&token=<jwt>` — queries `core_ride` rows from shared SQLite database.
- WebSocket for live GPS tracking:
  - `ws://<host>:8080/ws/gps?token=<jwt>` — send/receive JSON messages like `{"ride_id":1,"lat":..,"lng":..}`.
  - FastAPI validates the JWT using the same `CARPOOL_SECRET_KEY`.

Notes
- Database file: `carpool_django/carpool.db` is created when running migrations.
- This backend is headless; frontend apps (mobile/web) are expected to live in separate repositories and call these APIs.
