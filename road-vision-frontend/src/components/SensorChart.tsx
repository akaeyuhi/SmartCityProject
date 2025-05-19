import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import type { SensorPayload } from '../types/sensors';

interface Props {
  data: SensorPayload[];
}

const SensorChart: React.FC<Props> = ({ data }) => {
  const chartData = data
    .map((d) => ({
      time: new Date(d.agent_data.timestamp).toLocaleTimeString(),
      temp: d.agent_data.temperature.value,
      vib: d.agent_data.vibration.magnitude,
      aqi: d.agent_data.air_quality.aqi,
    }))
    .reverse();

  return (
    <LineChart width={800} height={300} data={chartData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="temp" name="Temp (°C)" />
      <Line type="monotone" dataKey="vib" name="Vibration" />
      <Line type="monotone" dataKey="aqi" name="AQI" />
    </LineChart>
  );
};

export default SensorChart;
