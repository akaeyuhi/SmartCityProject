from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    z = agent_data.accelerometer.z

    if abs(z) < 1.5:
        road_state = "normal"
    elif 1.5 <= abs(z) < 3.0:
        road_state = "bump"
    elif abs(z) >= 3.0:
        road_state = "hole"
    else:
        road_state = "unknown"

    return ProcessedAgentData(
        road_state=road_state,
        agent_data=agent_data
    )
