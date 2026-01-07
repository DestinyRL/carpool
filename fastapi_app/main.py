import os
import jwt
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DOCKER_ENV = os.environ.get('DOCKER_ENV')

if DOCKER_ENV:
    DB_CONFIG = {
        'dbname': os.environ.get('POSTGRES_DB', 'carpool'),
        'user': os.environ.get('POSTGRES_USER', 'carpool_user'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'carpool_password'),
        'host': os.environ.get('POSTGRES_HOST', 'db'),
        'port': os.environ.get('POSTGRES_PORT', '5432'),
    }
else:
    import sqlite3
    DATABASE = os.path.join(os.path.dirname(__file__), '..', 'carpool_django', 'carpool.db')

SECRET_KEY = os.environ.get('CARPOOL_SECRET_KEY', 'dev-secret-for-carpool-backend')

app = FastAPI(title='Carpool FastAPI Gateway')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RideSearchResult(BaseModel):
    id: int
    origin: str
    destination: str
    departure_time: str
    available_seats: int
    price_cents: int


def validate_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')


@app.get('/search', response_model=List[RideSearchResult])
def ride_search(q: str = '', token: str = ''):
    if token:
        validate_jwt(token)

    if DOCKER_ENV:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    query = "SELECT id, origin, destination, departure_time, available_seats, price_cents FROM core_ride"
    params = []
    if q:
        query += " WHERE origin LIKE %s OR destination LIKE %s" if DOCKER_ENV else " WHERE origin LIKE ? OR destination LIKE ?"
        params.extend([f"%{q}%", f"%{q}%"])
    
    cur.execute(query, params)
    rows = cur.fetchall()
    results = [dict(r) for r in rows]
    conn.close()
    return results


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket('/ws/gps')
async def gps_ws(websocket: WebSocket, token: str = ''):
    if token == '':
        await websocket.close(code=1008)
        return
    try:
        validate_jwt(token)
    except HTTPException:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "token" in data and "ride_id" in data:
                try:
                    validate_jwt(data["token"])
                    await manager.broadcast({"ride_id": data["ride_id"], "gps": data})
                except HTTPException:
                    await websocket.send_json({"error": "Invalid token"})
            else:
                await websocket.send_json({"error": "Token or ride_id missing"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
