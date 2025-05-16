import asyncio
import json
from typing import Set, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, DateTime
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, delete, update, insert
from datetime import datetime
from pydantic import BaseModel, field_validator
from pydantic.json import pydantic_encoder
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
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)

processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("user_id", Integer),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("magnitude", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("temperature", Float),
    Column("temp_unit", String),
    Column("humidity", Float),
    Column("illumination", Float),
    Column("pm2_5", Float),
    Column("pm10", Float),
    Column("aqi", Integer),
    Column("temp_status", String),
    Column("humidity_status", String),
    Column("vibration_status", String),
    Column("air_quality_status", String),
    Column("light_status", String),
    Column("timestamp", DateTime),
)
metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Pydantic models for WebSocket and CRUD
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float

class GpsData(BaseModel):
    latitude: float
    longitude: float

class TemperatureData(BaseModel):
    value: float
    unit: str

class HumidityData(BaseModel):
    value: float
    unit: str

class LightData(BaseModel):
    illumination: float

class AirQualityData(BaseModel):
    pm2_5: float
    pm10: float
    aqi: int

class VibrationData(AccelerometerData): 
    magnitude: float | None

class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    temperature: TemperatureData
    humidity: HumidityData
    vibration: VibrationData
    light: LightData
    air_quality: AirQualityData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except Exception:
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format."
            )

class ProcessedAgentDataIn(BaseModel):
    agent_data: AgentData
    road_state: str
    temp_status: str
    humidity_status: str
    vibration_status: str
    light_status: str
    air_quality_status: str

class ProcessedAgentDataOut(BaseModel):
    id: int
    road_state: str
    user_id: int
    x: float
    y: float
    z: float
    magnitude: float
    latitude: float
    longitude: float
    temperature: float
    temp_unit: str
    humidity: float
    humidity_unit: str
    illumination: float
    pm2_5: float
    pm10: float
    aqi: int
    temp_status: str
    humidity_status: str
    vibration_status: str
    light_status: str
    air_quality_status: str
    timestamp: datetime

# WebSocket subscriptions
subscriptions: Set[WebSocket] = set()

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)

async def send_data_to_subscribers(data: List[ProcessedAgentDataOut]):
    message = json.dumps([item.dict() for item in data], default=pydantic_encoder)
    for ws in subscriptions:
        await ws.send_text(message)

# CRUDL endpoints
@app.post("/processed_agent_data/", response_model=None)
async def create_processed_agent_data(data: List[ProcessedAgentDataIn]):
    with SessionLocal() as session:
        out_items: List[ProcessedAgentDataOut] = []
        for item in data:
            vals = item.agent_data
            query = insert(processed_agent_data).values(
                road_state=item.road_state,
                user_id=vals.user_id,
                x=vals.accelerometer.x,
                y=vals.accelerometer.y,
                z=vals.accelerometer.z,
                magnitude=vals.vibration.magnitude,
                latitude=vals.gps.latitude,
                longitude=vals.gps.longitude,
                temperature=vals.temperature.value,
                temp_unit=vals.temperature.unit,
                humidity=vals.humidity.value,
                humidity_unit=vals.humidity.unit,
                illumination=vals.light.illumination,
                pm2_5=vals.air_quality.pm2_5,
                pm10=vals.air_quality.pm10,
                aqi=vals.air_quality.aqi,
                temp_status=item.temp_status,
                humidity_status=item.humidity_status,
                vibration_status=item.vibration_status,
                light_status=item.light_status,
                air_quality_status=item.air_quality_status,
                timestamp=vals.timestamp,
            )
            result = session.execute(query)
            inserted_id = result.inserted_primary_key[0]
            out_items.append(
                ProcessedAgentDataOut(
                    id=inserted_id,
                    road_state=item.road_state,
                    user_id=vals.user_id,
                    x=vals.accelerometer.x,
                    y=vals.accelerometer.y,
                    z=vals.accelerometer.z,
                    magnitude=vals.vibration.magnitude,
                    latitude=vals.gps.latitude,
                    longitude=vals.gps.longitude,
                    temperature=vals.temperature.value,
                    temp_unit=vals.temperature.unit,
                    humidity=vals.humidity.value,
                    humidity_unit=vals.humidity.unit,
                    illumination=vals.light.illumination,
                    pm2_5=vals.air_quality.pm2_5,
                    pm10=vals.air_quality.pm10,
                    aqi=vals.air_quality.aqi,
                    temp_status=item.temp_status,
                    humidity_status=item.humidity_status,
                    vibration_status=item.vibration_status,
                    light_status=item.light_status,
                    air_quality_status=item.air_quality_status,
                    timestamp=vals.timestamp,
                )
            )
        session.commit()
    await send_data_to_subscribers(out_items)
    return {"status": "ok"}

@app.get("/processed_agent_data/{item_id}", response_model=ProcessedAgentDataOut)
def read_processed_agent_data(item_id: int):
    with SessionLocal() as session:
        query = select(processed_agent_data).where(
            processed_agent_data.c.id == item_id
        )
        result = session.execute(query).first()
        if not result:
            raise HTTPException(status_code=404, detail="Data not found")
        row = result._mapping
        return ProcessedAgentDataOut(**row)

@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataOut])
def list_processed_agent_data():
    with SessionLocal() as session:
        result = session.execute(select(processed_agent_data)).all()
        return [ProcessedAgentDataOut(**row._mapping) for row in result]

@app.put("/processed_agent_data/{item_id}", response_model=ProcessedAgentDataOut)
def update_processed_agent_data(item_id: int, data: ProcessedAgentDataIn):
    with SessionLocal() as session:
        vals = data.agent_data
        query = update(processed_agent_data).where(
            processed_agent_data.c.id == item_id
        ).values(
            road_state=data.road_state,
            user_id=vals.user_id,
            x=vals.accelerometer.x,
            y=vals.accelerometer.y,
            z=vals.accelerometer.z,
            magnitude=vals.vibration.magnitude,
            latitude=vals.gps.latitude,
            longitude=vals.gps.longitude,
            temperature=vals.temperature.value,
            temp_unit=vals.temperature.unit,
            humidity=vals.humidity.value,
            humidity_unit=vals.humidity.unit,
            illumination=vals.light.illumination,
            pm2_5=vals.air_quality.pm2_5,
            pm10=vals.air_quality.pm10,
            aqi=vals.air_quality.aqi,
            temp_status=data.temp_status,
            humidity_status=data.humidity_status,
            vibration_status=data.vibration_status,
            light_status=data.light_status,
            air_quality_status=data.air_quality_status,
            timestamp=vals.timestamp,
        )
        session.execute(query)
        session.commit()
        return read_processed_agent_data(item_id)

@app.delete("/processed_agent_data/{item_id}", response_model=ProcessedAgentDataOut)
def delete_processed_agent_data(item_id: int):
    with SessionLocal() as session:
        query = select(processed_agent_data).where(
            processed_agent_data.c.id == item_id
        )
        result = session.execute(query).first()
        if not result:
            raise HTTPException(status_code=404, detail="Data not found")
        row = result._mapping
        session.execute(delete(processed_agent_data).where(
            processed_agent_data.c.id == item_id
        ))
        session.commit()
        return ProcessedAgentDataOut(**row)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
