import asyncio
import json
from typing import Set, Dict, List, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, delete, update, insert
from datetime import datetime
from pydantic import BaseModel, field_validator
from config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)

# FastAPI app setup
app = FastAPI()

# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.bind = engine

# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("user_id", Integer),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
)
metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# FastAPI models
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float

class GpsData(BaseModel):
    latitude: float
    longitude: float

class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).")

class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

# SQLAlchemy model
class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str
    user_id: int
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime

# WebSocket subscriptions
subscriptions: Dict[int, Set[WebSocket]] = {}

# FastAPI WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in subscriptions:
        subscriptions[user_id] = set()
    subscriptions[user_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions[user_id].remove(websocket)

# Function to send data to subscribed users
async def send_data_to_subscribers(user_id: int, data):
    if user_id in subscriptions:
        for websocket in subscriptions[user_id]:
            await websocket.send_json(json.dumps(data))

# FastAPI CRUDL endpoints

@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    db = SessionLocal()
    new_entries = []
    for entry in data:
        agent = entry.agent_data
        stmt = insert(processed_agent_data).values(
            road_state=entry.road_state,
            user_id=agent.user_id,
            x=agent.accelerometer.x,
            y=agent.accelerometer.y,
            z=agent.accelerometer.z,
            latitude=agent.gps.latitude,
            longitude=agent.gps.longitude,
            timestamp=agent.timestamp
        ).returning(processed_agent_data.c.id)
        new_id = db.execute(stmt).scalar()
        new_entries.append({"id": new_id, **entry.dict()})

        await send_data_to_subscribers(agent.user_id, entry.dict())

    db.commit()
    db.close()
    return new_entries

@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    db = SessionLocal()
    stmt = select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
    result = db.execute(stmt).fetchone()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")
    return dict(zip(processed_agent_data.columns.keys(), result))

@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data():
    db = SessionLocal()
    stmt = select(processed_agent_data)
    results = db.execute(stmt).fetchall()
    db.close()
    return [dict(zip(processed_agent_data.columns.keys(), row)) for row in results]

@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    db = SessionLocal()
    agent = data.agent_data
    stmt = update(processed_agent_data).where(
        processed_agent_data.c.id == processed_agent_data_id
    ).values(
        road_state=data.road_state,
        user_id=agent.user_id,
        x=agent.accelerometer.x,
        y=agent.accelerometer.y,
        z=agent.accelerometer.z,
        latitude=agent.gps.latitude,
        longitude=agent.gps.longitude,
        timestamp=agent.timestamp
    ).returning(processed_agent_data.c.id)
    
    result = db.execute(stmt).scalar()
    db.commit()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")
    return read_processed_agent_data(processed_agent_data_id)

@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    db = SessionLocal()
    stmt = delete(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id).returning(processed_agent_data.c.id)
    result = db.execute(stmt).scalar()
    db.commit()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": f"Deleted record {processed_agent_data_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
