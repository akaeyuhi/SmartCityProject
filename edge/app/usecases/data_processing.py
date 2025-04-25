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
    raw_z  = agent_data.accelerometer.z
    g_z = raw_z / 16384
    abs_g_z = abs(g_z)

    if abs_g_z < 1.5:
        road_state = "normal"
    elif 1.5 <= abs_g_z < 3.0:
        road_state = "bump"
    elif abs_g_z >= 3.0:
        road_state = "hole"
    else:
        road_state = "unknown"

    # print(f"Detected: {road_state} | Raw Z: {raw_z} | g-force: {g_z:.2f}")

    return ProcessedAgentData(
        road_state=road_state,
        agent_data=agent_data
    )
