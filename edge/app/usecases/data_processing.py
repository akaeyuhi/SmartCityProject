from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData

BUMP_THRESHOLD = 7000    # Z > 7000 ⇒ bump
POTHOLE_THRESHOLD = -7000  # Z < -7000 ⇒ pothole


def process_agent_data(agent_data: AgentData, 
                       bump_threshold: float = BUMP_THRESHOLD, 
                       pothole_threshold: float = POTHOLE_THRESHOLD) -> ProcessedAgentData:
    """
    Process all sensors and classify their status along with road_state.
    """
    # Classify road state based on vibration magnitude
    vib_mag = agent_data.vibration.magnitude
    if vib_mag < 1.0:
        vibration_road = 'smooth'
    elif vib_mag < 3.0:
        vibration_road = 'moderate'
    else:
        vibration_road = 'rough'

    # Temperature status
    temp = agent_data.temperature.value
    if temp < 0:
        temp_stat = 'freezing'
    elif temp < 20:
        temp_stat = 'cool'
    elif temp < 30:
        temp_stat = 'warm'
    else:
        temp_stat = 'hot'

    # Humidity status
    hum = agent_data.humidity.value
    if hum < 30:
        hum_stat = 'dry'
    elif hum < 60:
        hum_stat = 'normal'
    else:
        hum_stat = 'humid'

    # Light status
    illum = agent_data.light.illumination
    light_stat = 'dark' if illum < 50 else 'well-lit'

    # Air quality status
    aqi = agent_data.air_quality.aqi
    if aqi is None:
        aq_stat = 'unknown'
    elif aqi <= 50:
        aq_stat = 'good'
    elif aqi <= 100:
        aq_stat = 'moderate'
    else:
        aq_stat = 'poor'

    z = agent_data.accelerometer.z

    if z > bump_threshold:
        road_state = "bump"
    elif z < pothole_threshold:
        road_state = "pothole"
    else:
        road_state = "normal"

    return ProcessedAgentData(
        agent_data=agent_data,
        road_state=road_state,
        temp_status=temp_stat,
        humidity_status=hum_stat,
        vibration_status=vibration_road,
        light_status=light_stat,
        air_quality_status=aq_stat,
    )
