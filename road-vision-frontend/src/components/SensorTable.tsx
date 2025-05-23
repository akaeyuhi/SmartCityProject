import React from 'react';
import type { SensorPayload } from '../types/sensors';

interface Props {
  data: SensorPayload[];
}

const SensorTable: React.FC<Props> = ({ data }) => (
  <div className="overflow-auto">
    <table className="min-w-full bg-white shadow rounded">
      <thead>
        <tr className="bg-gray-100 text-center">
          <th className="p-2">Time</th>
          <th className="p-2">Road</th>
          <th className="p-2">Temp</th>
          <th className="p-2">Hum</th>
          <th className="p-2">Vib</th>
          <th className="p-2">AQI</th>
        </tr>
      </thead>
      <tbody>
        {data.map((d, i) => (
          <tr key={i} className="border-t hover:bg-gray-50 text-center">
            <td className="p-2">
              {new Date(d.agent_data.timestamp).toLocaleTimeString()}
            </td>
            <td className="p-2 capitalize">{d.road_state}</td>
            <td className="p-2">
              <span className="font-mono">
                {d.agent_data.temperature.value}
                {d.agent_data.temperature.unit}
              </span>
              <span className="ml-2 badge">{d.temp_status}</span>
            </td>
            <td className="p-2">
              {d.agent_data.humidity.value}%{' '}
              <span className="badge">{d.humidity_status}</span>
            </td>
            <td className="p-2">
              {d.agent_data.vibration.magnitude.toFixed(2)}{' '}
              <span className="badge">{d.vibration_status}</span>
            </td>
            <td className="p-2">
              {d.agent_data.air_quality.aqi}{' '}
              <span className="badge">{d.air_quality_status}</span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default SensorTable;
