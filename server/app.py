from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).parent / "environment.db"

app = FastAPI(title="IoT Environmental Station API", version="0.1.0")


class SensorReading(BaseModel):
    node_id: str = Field(min_length=1, max_length=64)
    temperature_c: float
    humidity_percent: float = Field(ge=0, le=100)
    pressure_hpa: float = Field(gt=0)
    light_lux: float = Field(ge=0)
    recorded_at: datetime | None = None


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                temperature_c REAL NOT NULL,
                humidity_percent REAL NOT NULL,
                pressure_hpa REAL NOT NULL,
                light_lux REAL NOT NULL,
                recorded_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/readings", status_code=201)
def create_reading(reading: SensorReading) -> dict:
    recorded_at = reading.recorded_at or datetime.now(timezone.utc)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO readings (
                node_id,
                temperature_c,
                humidity_percent,
                pressure_hpa,
                light_lux,
                recorded_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                reading.node_id,
                reading.temperature_c,
                reading.humidity_percent,
                reading.pressure_hpa,
                reading.light_lux,
                recorded_at.isoformat(),
            ),
        )
        connection.commit()
        reading_id = cursor.lastrowid

    return {"id": reading_id, **reading.model_dump(), "recorded_at": recorded_at}


@app.get("/api/readings/latest")
def latest_reading(node_id: str | None = None) -> dict:
    query = "SELECT * FROM readings"
    params: tuple = ()

    if node_id:
        query += " WHERE node_id = ?"
        params = (node_id,)

    query += " ORDER BY recorded_at DESC LIMIT 1"

    with get_connection() as connection:
        row = connection.execute(query, params).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="No readings found")

    return dict(row)


@app.get("/api/readings")
def list_readings(node_id: str | None = None, limit: int = 100) -> list[dict]:
    limit = max(1, min(limit, 1000))
    query = "SELECT * FROM readings"
    params: list = []

    if node_id:
        query += " WHERE node_id = ?"
        params.append(node_id)

    query += " ORDER BY recorded_at DESC LIMIT ?"
    params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [dict(row) for row in rows]
