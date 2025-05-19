import React, { useEffect, useRef, useState } from 'react';
import { useMqttClient } from '../hooks/useMqttClient';
import SensorTable from './SensorTable';
import SensorChart from './SensorChart';
import SensorCard from './SensorCard';
import type { SensorPayload } from '../types/sensors.ts';

const MQTT_URL = import.meta.env.VITE_MQTT_URL || 'ws://localhost:9001';
const TOPIC = 'processed_data_topic';
const REFRESH_INTERVAL = 5000;

const Dashboard: React.FC = () => {
  const { data: incomingData, error } = useMqttClient(MQTT_URL, TOPIC);
  const [dataHistory, setDataHistory] = useState<SensorPayload[]>([]);
  const bufferRef = useRef<SensorPayload[]>([]);
  const latest = dataHistory[0];

  useEffect(() => {
    bufferRef.current = incomingData;
  }, [incomingData]);

  // Оновлюємо стан даних раз в 10 секунд
  useEffect(() => {
    const timer = setInterval(() => {
      if (bufferRef.current.length > 0) {
        const slice = bufferRef.current.slice(0, 50);
        setDataHistory(slice);
      }
    }, REFRESH_INTERVAL);

    return () => clearInterval(timer);
  }, []);

  if (error) {
    return <div className="p-4 text-red-600">Error: {error.message}</div>;
  }

  if (!latest) {
    return <div className="p-4">No data available yet...</div>;
  }

  // eslint-disable-next-line camelcase
  const { temperature, humidity, air_quality, light, vibration } =
    latest.agent_data;

  // Конфігурація карток
  const cardConfigs = [
    {
      title: 'Road State',
      value: latest.road_state,
      status: latest.road_state,
    },
    {
      title: 'Temperature',
      value: temperature.value,
      unit: temperature.unit,
      status: latest.temp_status,
    },
    {
      title: 'Humidity',
      value: humidity.value,
      unit: '%',
      status: latest.humidity_status,
    },
    {
      title: 'Vibration (mag)',
      value: vibration.magnitude.toFixed(2),
      status: latest.vibration_status,
    },
    {
      title: 'Illumination ',
      value: light.illumination,
      unit: 'lux',
      status: latest.light_status,
    },
    {
      title: 'Air Quality (AQI)',
      // eslint-disable-next-line camelcase
      value: air_quality.aqi,
      status: latest.air_quality_status,
    },
  ];

  return (
    <div className="p-4 grid grid-cols-1 gap-6">
      <h1 className="text-2xl font-bold">IoT Road Vision Dashboard</h1>

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
      <SensorChart data={dataHistory} />
      <SensorTable data={dataHistory} />
    </div>
  );
};

export default Dashboard;
