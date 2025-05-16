from pydantic import BaseModel
from app.entities.agent_data import AgentData


class ProcessedAgentData(BaseModel):
    agent_data: AgentData
    road_state: str
    temp_status: str | None = None
    humidity_status: str | None = None
    vibration_status: str | None = None
    light_status: str | None = None
    air_quality_status: str | None = None
