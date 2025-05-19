export interface AccelerometerData {
  x: number;
  y: number;
  z: number;
}
export interface GpsData {
  latitude: number;
  longitude: number;
}
export interface TemperatureData {
  value: number;
  unit: 'C' | 'F';
}
export interface HumidityData {
  value: number;
  unit: '%';
}
export interface VibrationData extends AccelerometerData {
  magnitude: number;
}
export interface LightData {
  illumination: number;
}
export interface AirQualityData {
  pm2_5: number;
  pm10: number;
  aqi: number;
}

export interface AgentData {
  user_id: number;
  accelerometer: AccelerometerData;
  gps: GpsData;
  temperature: TemperatureData;
  humidity: HumidityData;
  vibration: VibrationData;
  light: LightData;
  air_quality: AirQualityData;
  timestamp: string;
}

export interface SensorPayload {
  agent_data: AgentData;
  road_state: string;
  air_quality_status: string;
  humidity_status: string;
  light_status: string;
  temp_status: string;
  vibration_status: string;
}
