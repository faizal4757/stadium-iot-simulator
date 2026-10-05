import json
import os
import time

import paho.mqtt.client as mqtt

from config import SENSORS, STADIUMS
from sensor_generator import generate_reading


PUBLISH_INTERVAL = 0.1

AWS_IOT_ENDPOINT = "a2laq814tgmnit-ats.iot.us-east-1.amazonaws.com"
AWS_IOT_PORT = 8883

CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")

CA_CERT = os.path.join(CERT_DIR, "AmazonRootCA1.pem")
CLIENT_CERT = os.path.join(CERT_DIR, "device-certificate.pem.crt")
PRIVATE_KEY = os.path.join(CERT_DIR, "private.pem.key")

MQTT_TOPIC = "stadium/iot/events"


last_run = {
    sensor["sensor_id"]: 0
    for sensor in SENSORS
}


stadium_state = {}

for sensor in SENSORS:
    key = (sensor["stadium_id"], sensor["zone"])

    if key not in stadium_state:
        stadium_state[key] = {
            "crowd_density": 1.5
        }


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to AWS IoT Core")
        print(f"MQTT topic: {MQTT_TOPIC}")
    else:
        print(f"MQTT connection failed: {reason_code}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="stadium-iot-simulator"
)

client.on_connect = on_connect

client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=PRIVATE_KEY
)

print("Stadium sensor simulator starting...")
print(f"Stadiums: {len(STADIUMS)}")
print(f"Sensor instances: {len(SENSORS)}")
print(f"AWS IoT endpoint: {AWS_IOT_ENDPOINT}")
print(f"MQTT topic: {MQTT_TOPIC}")
print()


client.connect(
    AWS_IOT_ENDPOINT,
    AWS_IOT_PORT,
    keepalive=60
)

client.loop_start()


try:
    while True:
        current_time = time.time()

        for sensor in SENSORS:
            sensor_id = sensor["sensor_id"]

            key = (
                sensor["stadium_id"],
                sensor["zone"]
            )

            if current_time - last_run[sensor_id] >= sensor["interval"]:

                reading = generate_reading(
                    sensor,
                    stadium_state[key]
                )

                if sensor["sensor_type"] == "crowd_density":
                    stadium_state[key]["crowd_density"] = reading["value"]

                event_json = json.dumps(reading)

                result = client.publish(
                    MQTT_TOPIC,
                    event_json,
                    qos=1
                )

                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"Published: {event_json}")
                else:
                    print(
                        f"Publish failed: {result.rc}"
                    )

                last_run[sensor_id] = current_time

        time.sleep(PUBLISH_INTERVAL)

except KeyboardInterrupt:
    print("\nStadium sensor simulator stopped.")

finally:
    client.loop_stop()
    client.disconnect()