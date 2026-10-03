import time
import json

from config import SENSORS, STADIUMS
from sensor_generator import generate_reading


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

                print(json.dumps(reading, indent=2))

                last_run[sensor_id] = current_time

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStadium sensor simulator stopped.")