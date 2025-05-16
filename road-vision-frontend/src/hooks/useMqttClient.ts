import { useState, useEffect } from 'react';
import mqtt from 'mqtt';
import type { MqttClient } from 'mqtt';
import type { SensorPayload } from '../types/sensors';

interface UseMqttResult {
  client: MqttClient | null;
  data: SensorPayload[];
  error: Error | null;
}

export function useMqttClient(
    brokerUrl: string,
    topic: string
): UseMqttResult {
  const [client, setClient] = useState<MqttClient | null>(null);
  const [data, setData] = useState<SensorPayload[]>([]);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // connect over WebSocket on the correct path
    const mqttClient = mqtt.connect(brokerUrl, {
      protocol: 'ws',
      reconnectPeriod: 1000,
      connectTimeout: 4000,
    });

    const handleConnect = () => {
      console.log('✅ MQTT connected');
      mqttClient.subscribe(topic, (err) => {
        if (err) console.error('Subscribe error:', err);
      });
    };

    const handleError = (err: Error) => {
      console.error('❌ MQTT error:', err);
      setError(err);
    };

    const handleMessage = (_topic: string, message: Buffer) => {
      try {
        const payload = JSON.parse(message.toString()) as SensorPayload;
        setData((prev) => [payload, ...prev].slice(0, 100)); // keep last 100
      } catch (e: any) {
        console.error('Failed to parse MQTT message', e);
      }
    };

    mqttClient.on('connect', handleConnect);
    mqttClient.on('error', handleError);
    mqttClient.on('message', handleMessage);

    setClient(mqttClient);

    return () => {
      mqttClient.off('connect', handleConnect);
      mqttClient.off('error', handleError);
      mqttClient.off('message', handleMessage);
      mqttClient.end(true);
    };
  }, [brokerUrl, topic]);

  return { client, data, error };
}
