import random
import uuid
from datetime import datetime, timezone

from config import STADIUMS


def generate_reading(sensor, stadium_state):
    sensor_type = sensor["sensor_type"]

    min_value = sensor["min"]
    max_value = sensor["max"]

    if sensor_type == "crowd_density":
        value = random.uniform(min_value, max_value)

    elif sensor_type == "temperature":
        crowd = min(stadium_state["crowd_density"] / 4, 1)
        value = min_value + (max_value - min_value) * (0.3 + 0.4 * crowd)
        value += random.uniform(-1, 1)

    elif sensor_type == "co2":
        crowd = min(stadium_state["crowd_density"] / 4, 1)
        value = min_value + (max_value - min_value) * (0.2 + 0.6 * crowd)
        value += random.uniform(-50, 50)

    else:
        value = random.uniform(min_value, max_value)

    # Simulate occasional anomalies
    anomaly = random.random() < 0.05

    if anomaly:
        value = max_value * random.uniform(1.5, 2)

    stadium = STADIUMS[sensor["stadium_id"]]

    return {
        "event_id": str(uuid.uuid4()),
        "stadium_id": sensor["stadium_id"],
        "stadium_name": stadium["stadium_name"],
        "sensor_id": sensor["sensor_id"],
        "sensor_type": sensor_type,
        "zone": sensor["zone"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "value": round(value, 2),
        "unit": sensor["unit"],
        "is_anomaly": anomaly
    }