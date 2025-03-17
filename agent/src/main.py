from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.parking_schema import ParkingSchema 
from file_datasource import FileDatasource
import config

def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc) # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client

def publish(client, topic_aggregated, topic_parking, datasource, delay):
    datasource.startReading()
    while True:
        time.sleep(delay)
        data = datasource.read()
        if data is None:
            continue

        aggregated_msg = AggregatedDataSchema().dumps(data["aggregated_data"])
        parking_msg = ParkingSchema().dumps(data["parking_data"])

        result1 = client.publish(topic_aggregated, aggregated_msg)
        result2 = client.publish(topic_parking, parking_msg)

        if result1[0] != 0:
            print(f"Failed to send aggregated data to topic {topic_aggregated}")
        if result2[0] != 0:
            print(f"Failed to send parking data to topic {topic_parking}")

def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)

    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")

    # Infinity publish data into two topics
    publish(client, config.MQTT_TOPIC, config.MQTT_PARKING_TOPIC, datasource, config.DELAY)

if __name__ == "__main__":
    run()
