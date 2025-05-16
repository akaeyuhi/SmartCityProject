import { useState, useEffect } from 'react';
import mqtt, { MqttClient } from 'mqtt';
//import { SensorPayload } from '../types/sensors';

export function useMqttClient(
    brokerUrl: string,
    topic: string
): MqttClient | null {
  const [client, setClient] = useState<MqttClient | null>(null);

  useEffect(() => {
    const mqttClient = mqtt.connect(brokerUrl, { reconnectPeriod: 1000 });
    mqttClient.on('connect', () => {
      console.log('MQTT connected');
      mqttClient.subscribe(topic);
    });
    mqttClient.on('error', (err) => console.error('MQTT error:', err));
    setClient(mqttClient);

    return () => {
      mqttClient.end();
    };
  }, [brokerUrl, topic]);

  return client;
}

// client.on('message', (topic, msg) => {
//   const data: SensorPayload = JSON.parse(msg.toString());
//   // оновити стейт
// });
