export interface AccelerometerData { x: number; y: number; z: number; magnitude: number; }
export interface GpsData { latitude: number; longitude: number; }
export interface TemperatureData { value: number; unit: 'C' | 'F'; status: string; }
export interface HumidityData { value: number; unit: '%'; status: string; }
export interface VibrationData { x: number; y: number; z: number; magnitude: number; status: string; }
export interface LightData { illumination: number; status: string; }
export interface AirQualityData { pm2_5: number; pm10: number; aqi: number; status: string; }

export interface SensorPayload {
  user_id: number;
  timestamp: string;
  road_state: string;
  accelerometer: AccelerometerData;
  gps: GpsData;
  temperature: TemperatureData;
  humidity: HumidityData;
  vibration: VibrationData;
  light: LightData;
  air_quality: AirQualityData;
}
