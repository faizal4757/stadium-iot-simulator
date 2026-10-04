
import time
import json
import boto3

from config import SENSORS, STADIUMS
from sensor_generator import generate_reading


# Kinesis configuration
STREAM_NAME = "stadium-iot-events"
AWS_REGION = "us-east-1"

kinesis = boto3.client(
    "kinesis",
    region_name=AWS_REGION
)


# Track the last execution time for each sensor
last_run = {
    sensor["sensor_id"]: 0
    for sensor in SENSORS
}


# Maintain separate crowd-density state for each stadium and zone
stadium_state = {}

for sensor in SENSORS:
    key = (sensor["stadium_id"], sensor["zone"])

    if key not in stadium_state:
        stadium_state[key] = {
            "crowd_density": 1.5
        }


print("Stadium sensor simulator started...")
print(f"Stadiums: {len(STADIUMS)}")
print(f"Sensor instances: {len(SENSORS)}")
print(f"Kinesis stream: {STREAM_NAME}")
print(f"AWS region: {AWS_REGION}")
print("Press Ctrl+C to stop.\n")


try:
    while True:
        current_time = time.time()

        for sensor in SENSORS:
            sensor_id = sensor["sensor_id"]
            key = (sensor["stadium_id"], sensor["zone"])

            if current_time - last_run[sensor_id] >= sensor["interval"]:
                reading = generate_reading(
                    sensor,
                    stadium_state[key]
                )

                # Update crowd state for this stadium and zone
                if sensor["sensor_type"] == "crowd_density":
                    stadium_state[key]["crowd_density"] = reading["value"]

                # Convert event to JSON
                event_json = json.dumps(reading)

                # Publish event to Kinesis
                response = kinesis.put_record(
                    StreamName=STREAM_NAME,
                    Data=event_json,
                    PartitionKey=reading["sensor_id"]
                )

                print(
                    f"Published: {reading['sensor_type']} | "
                    f"Sensor: {sensor_id} | "
                    f"Shard: {response['ShardId']} | "
                    f"Sequence: {response['SequenceNumber']}"
                )

                last_run[sensor_id] = current_time

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStadium sensor simulator stopped.")

except Exception as error:
    print(f"\nSimulator stopped due to an error: {error}")
    raise