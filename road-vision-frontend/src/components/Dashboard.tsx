import React, { useState, useEffect } from 'react';
import { useMqttClient } from '../hooks/useMqttClient';
import type {SensorPayload} from '../types/sensors';
import SensorTable from './SensorTable';
import SensorChart from './SensorChart';
import SensorCard from './SensorCard';

const MQTT_URL = 'ws://mqtt:9001';
const TOPIC = 'processed_data_topic';

const Dashboard: React.FC = () => {
  const client = useMqttClient(MQTT_URL, TOPIC);
  const [dataHistory, setDataHistory] = useState<SensorPayload[]>([]);
  const latest = dataHistory[0];

  useEffect(() => {
    if (!client) return;
    const handler = (_topic: string, message: Buffer) => {
      const payload: SensorPayload = JSON.parse(message.toString());
      setDataHistory(prev => [payload, ...prev].slice(0, 50));
    };
    client.on('message', handler);
    return () => { client.off('message', handler); };
  }, [client]);

  const cardConfigs = latest
      ? [
        { title: 'Road State', value: latest.road_state, status: latest.road_state },
        { title: 'Temperature', value: latest.temperature.value, unit: latest.temperature.unit, status: latest.temperature.status },
        { title: 'Humidity', value: latest.humidity.value, unit: '%', status: latest.humidity.status },
        { title: 'Vibration (mag)', value: latest.vibration.magnitude.toFixed(2), status: latest.vibration.status },
        { title: 'Illumination', value: latest.light.illumination, unit: 'lux', status: latest.light.status },
        { title: 'Air Quality (AQI)', value: latest.air_quality.aqi, status: latest.air_quality.status },
      ]
      : [];

  return (
      <div className="p-4 grid grid-cols-1 gap-6">
        <h1 className="text-2xl font-bold">IoT Road Vision Dashboard</h1>

        {latest && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {cardConfigs.map(({ title, value, unit, status }) => (
                  <SensorCard
                      key={title}
                      title={title}
                      value={value}
                      unit={unit}
                      status={status}
                  />
              ))}
            </div>
        )}

        {/* Historical table and chart */}
        <SensorTable data={dataHistory} />
        <SensorChart data={dataHistory} />
      </div>
  );
};

export default Dashboard;
